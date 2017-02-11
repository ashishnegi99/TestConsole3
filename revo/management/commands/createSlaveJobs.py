from django.core.management.base import BaseCommand, CommandError
from sets import Set
from app.jenkinsapp import JenkinsApp
from revo.models import device as STBs
import requests as Requests
from revo.models import device as stb_devices
import jenkins
import json

class Command(BaseCommand):
    help = 'Create a cron job for slaves used in the database'

    def handle(self, *args, **options):
        self.createActiveSTBList()

    def daemon_job(self):
        slaves = Set([])
        device_list = STBs.objects.all()
        for device in device_list:
            slaves.add(device.host)

        jnkns_server = JenkinsApp('http://localhost:8080', 'jenkins', 'jenkins123')
        job_list = jnkns_server.get_jobs_list("/job/revo/job/cron/job/")
        slave_job_list = Set([job[u'fullname'].split('/')[2] for job in job_list])
        
        #For all slaves in DB but no cronjob
        for slave in (slaves - slave_job_list):
            self.create_jnkns_cron_job(jnkns_server, slave)
            print "I was ADDED: " + slave

        #Delete cron job if exists for all slaves not in DB
        for slave in (slave_job_list - slaves):
            print slave
            jnkns_server.delete_job(slave, "revo/cron")
            print "I was DELETED: " + slave


    def create_jnkns_cron_job(self, jnkns_obj, host_name):
        mycommand = "python test_stb.py " + "%WORKSPACE%"
        jnkns_obj.create_jnkns_cron_job("revo/cron", host_name, mycommand)

    
    def createActiveSTBList(self):
        #Copy all files from master jenkins
        jnkns_server = JenkinsApp('http://localhost:8080', 'jenkins', 'jenkins123')
        job_list = jnkns_server.get_jobs_list("/job/revo/job/cron/job/")
        sn_url_list = [job[u'url'] + 'ws/serialnumbers.txt' for job in job_list]

        online_devices = Set()
        for sn in sn_url_list:
            print sn
            res = Requests.get(sn, auth=('jenkins', 'jenkins123')) 
            if(res.status_code == 200):
                device_serial_num_list = res.text.split(',')
                device_serial_num_list
                online_devices = online_devices.union(Set(device_serial_num_list))

        print str(online_devices)
        self.creatSTBStatusJson(online_devices)


    def creatSTBStatusJson(self, online_devices):
        device_list = stb_devices.objects.all()

        # Check if all stbs exists in the db
        matched_device = Set([row.unit_address for row in device_list]).intersection(online_devices)
               
        # Get current jenkins status of the build coressponding to each STB
        jnkns_server = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
        running_builds = jnkns_server.get_running_builds()
        running_builds_path = [ urlparse(build['url']).path for build in running_builds if REVO_FOLDER_PATH in build['url']]
        
        # Create status json array
        sample_list = []
        for device in device_list:
            sample_dict = {}

            if device.unit_address in matched_device:
                full_path = "/job/revo/job/" + device.name
                if any( path.startswith(full_path) for path in running_builds_path):
                    sample_dict["STBStatus"] = 2
                else:
                    sample_dict["STBStatus"] = 1
            else:
                sample_dict["STBStatus"] = 0

            sample_dict["Env"] = device.environment.name
            sample_dict["STBLabel"] = device.name
            sample_dict["UnitAdd"] = device.unit_address
            sample_list.append(sample_dict)

        #commit the file
        jsonfile = open('revo/templates/revo/JSON/STBStatus.json', 'w')
        out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in sample_list]) + "\n]"
        jsonfile.write(out)