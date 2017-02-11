from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.db.models import Sum, Avg, Count
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from app.forms import UserForm, BootstrapAuthenticationForm
from app.models import Storm, Appium, racktestresult
from revo.models import TestSuite
from revo.models import device as stb_devices
from revo.models import TestCase, Config
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse
from django.core.exceptions import ValidationError
from ftplib import FTP
from app.jenkinsapp import JenkinsApp
from revo.testsuitejson import TestSuiteJson
from urlparse import urlparse
import jenkins
import urllib2
import urllib
import socket
import time
import string
import re
import os
import io
import csv
import json
import json as simplejson
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

REVO_FOLDER_PATH = "/job/revo/job/"
REVO_FOLDER_NAME = "revo"

@login_required
def home(request):
    assert isinstance(request, HttpRequest)
    test_suite_list = [suite.name for suite in TestSuite.objects.all()]

    return render(
        request,
        "revo/revo.html",
        RequestContext(request, {
            "test_suite_list" : test_suite_list,
        })
    )

def  consolelink(request):
    assert isinstance(request, HttpRequest)
    job = request.GET["job"]
    build = int(request.GET["build"])
    server = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    output = server.get_build_console_output(get_full_job_name(job), build)
    return HttpResponse(output)


def revo_view(request):
    my_stb = request.POST.getlist('check1')
    my_test_suite = request.POST.getlist('checks')
    user_name = request.user.username
    
    with open("revo_configs.txt") as revo_config:
        content = revo_config.read().splitlines()
    
    loc_fix = content[0]
    test_runner_path = content[1]
    report_location = content[2]
    run_path = content[3]
    json_path = content[4]
    env_variables = "%JOB_NAME% %BUILD_TAG% SIT"
    path_build = "cd %BUILD_PATH%"

    cd1 = "<command>"
    cd2 = "</command>"

    job_node_list = {}
    for row in stb_devices.objects.all():
        job_node_list[row.name] = row.host

    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    new_job_config_pre =    "<?xml version='1.0' encoding='UTF-8'?><project><actions/><description></description><keepDependencies>false</keepDependencies><properties><hudson.model.ParametersDefinitionProperty><parameterDefinitions><hudson.model.StringParameterDefinition><name>param1</name><description></description><defaultValue></defaultValue></hudson.model.StringParameterDefinition><hudson.model.StringParameterDefinition><name>param2</name><description></description><defaultValue></defaultValue></hudson.model.StringParameterDefinition></parameterDefinitions></hudson.model.ParametersDefinitionProperty></properties><scm class='hudson.scm.NullSCM'/>"
    new_job_config_post = "<disabled>false</disabled><blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding><blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding><triggers/><concurrentBuild>false</concurrentBuild><builders><hudson.tasks.BatchFile><command>timeout 500</command></hudson.tasks.BatchFile></builders><publishers/><buildWrappers/></project>"
    new_folder_config = '<com.cloudbees.hudson.plugins.folder.Folder plugin="cloudbees-folder@5.13"><actions/><description/><displayName>revo</displayName><properties/><views><hudson.model.AllView><owner class="com.cloudbees.hudson.plugins.folder.Folder" reference="../../.."/><name>All</name><filterExecutors>false</filterExecutors><filterQueue>false</filterQueue><properties class="hudson.model.View$PropertyList"/></hudson.model.AllView></views><viewsTabBar class="hudson.views.DefaultViewsTabBar"/><healthMetrics><com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric/></healthMetrics><icon class="com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon"/></com.cloudbees.hudson.plugins.folder.Folder>'

    if j.job_exists('revo') != True:
        j.create_job('revo', new_folder_config)

    count1 = 0
    for s in my_stb:
        count2 = 0
        for t in my_test_suite:
            job_path = "revo/" + my_stb[count1]
            logger.debug("JOB_PATH: " + job_path + ' : ' + str(my_test_suite[count2]))
            mycommand2 = cd1 + "set " + loc_fix + "\n" + "cd " + test_runner_path + "\n" + "python TestRunner.py " + "%param1%" + " " + my_stb[count1] + " True " + report_location + " " + run_path + " " + json_path + " " + env_variables + "\n" + path_build + cd2
            logger.debug("MyCommand2: " +  mycommand2)

            new_job_config = new_job_config_pre
            if my_stb[count1] in job_node_list.keys() and job_node_list[my_stb[count1]]:
                new_job_config += "<assignedNode>" + job_node_list[my_stb[count1]] + "</assignedNode><canRoam>false</canRoam>"
            else :
                new_job_config += "<canRoam>true</canRoam>"
            new_job_config += new_job_config_post

            if not j.job_exists(job_path):
                j.create_job(job_path, new_job_config)
            else:
                j.reconfig_job(job_path, new_job_config)

            j.enable_job(job_path)
            jobConfig = j.get_job_config(job_path)

            tree = ET.XML(jobConfig)
            with open("temp.xml", "w") as f:
                f.write(ET.tostring(tree))
            
            document = parse('temp.xml')
            actors = document.getElementsByTagName("command")
            
            for act in actors:
                for node in act.childNodes:
                    if node.nodeType == node.TEXT_NODE:
                        r = "{}".format(node.data)
            
            prev_command = cd1 + r + cd2
            
            shellCommand = jobConfig.replace(prev_command, mycommand2)
            #TODO: check this should not be required if we pass the cmd in the confguration itself
            j.reconfig_job(job_path, shellCommand)
            
            j.build_job(job_path,{'param1': my_test_suite[count2],'param2': user_name})
            count2 = count2+1    
        count1 = count1+1
 
    return HttpResponseRedirect("/revo")
 

def run_job(request):
    post_data = json.loads(request.body)
    #parsing data
    scheduled = True if (post_data['scheduled'] == 'true') else False
    stbs = post_data['stbs']
    test_suites = post_data['suites']
    test_suite_names = [ suite["name"] for suite in test_suites]
    user_name = request.user.username

    #create TestSuite.json
    revo_test_json = TestSuiteJson()
    #cache this part
    for stb_name in stbs:
        stb = None
        if stb_devices.objects.filter(name=stb_name).exists():
            #TODO: check if the name is in the active stb list
            stb = stb_devices.objects.get(name=stb_name)
            revo_test_json.append_box(stb_name,ip=stb.ip,unit_address=stb.unit_address,terminal_id=stb.terminal_id,client_ip=stb.client_ip,type=stb.device_type)
        
    for test_suite in test_suites:
        #TODO: check if the name and testcases are in the db
        revo_test_json.append_suite(test_suite["name"], test_suite["cases"])

    #TODO: put this file on some ftp server and then pass it path in the cmd
    print revo_test_json.get_json()
    slave_configs = get_revo_configs()    
    jnkns_app = JenkinsApp('http://localhost:8080', 'jenkins', 'jenkins123')

    for stb_name in stbs:
        for test_suite in test_suites:
            stb_details = None
            if stb_devices.objects.filter(name=stb_name).exists():
                #TODO: check if the name is in the active stb list
                stb_details = stb_devices.objects.get(name=stb_name)
            else:
                pass    
                #TODO SET error code HttpResponseBadRequest and return
            
            if(stb_details and stb_details.environment.name in slave_configs):
                config = slave_configs[stb_details.environment.name]
                jnknscommand = ( "set " + config["loc_fix"] + "\n" + "cd " + config["runner_path"] + "\n" + "python TestRunner.py " 
                                + "%param1%" + " " + stb_name + " True " + config["report_loc"] + " " + config["run_path"] + " " 
                                + config["json_path"] + " " + config["env_var"] + "\n" + config["build_path"] )

                if scheduled: 
                    scheduled_time = datetime.strptime(post_data['time'], "%m/%d/%Y %H:%M %p")
                    time_diff = scheduled_time - datetime.now()
                    time_diff_in_sec = int(time_diff.total_seconds())

                    if time_diff_in_sec > 1:
                        jobs_scheduled = []
                        jobs_scheduled.append(jnkns_app.create_groovy_job(stb_name, time_diff_in_sec, param1=test_suite["name"], param2=user_name))
                        jstr = json.dumps(jobs_scheduled)
                        jnkns_app.schedule_job(jstr)
                else:
                    jnkns_app.create_job(stb_name, REVO_FOLDER_NAME, False, stb_details.host, jnknscommand, scheduled, test_suite["name"], user_name)
            else:
                pass

    return HttpResponse("data", content_type='application/text')
    

def get_revo_configs():
    slave_configs = {}

    config_list = Config.objects.all()
    
    for content in config_list:    
        config = {}
        config["loc_fix"] = content.loc_fix
        config["runner_path"] = content.test_runner_path
        config["report_loc"] = content.report_location
        config["run_path"] = content.run_path
        config["json_path"] = content.json_path
        config["env_var"] = "%JOB_NAME% %BUILD_TAG% SIT"
        config["build_path"] = "cd %BUILD_PATH%"
        slave_configs[content.name] =  config
    
    return slave_configs

# from sets import Set
# def daemon_job():
#     slaves = Set([])
#     device_list = stb_devices.objects.all()
#     for device in device_list:
#         slaves.add(device.host)

#     jnkns_server = JenkinsApp('http://localhost:8080', 'jenkins', 'jenkins123')
#     job_list = jnkns_app.get_jobs_list("/job/revo/job/cron/job/")
#     slave_job_list = Set([job[u'fullname'] for job in job_list])
    
#     #For all slaves in DB but no cronjob
#     for slave in (slaves - slave_job_list):
#         create_jnkns_cron_job(jnkns_server, slave)

#     #Delete cron job if exists for all slaves not in DB
#     for slave in (slave_job_list - slaves):
#         jnkns_server.delete_job('slave', "revo/cron")
    
# def create_jnkns_cron_job(jnkns_obj, host_name):
#     mycommand = "python test_stb.py " + "%WORKSPACE%"
#     param['name'] = "test_stb.py"
#     param['value'] = param['name'] 
#     param['type'] =  "File"
#     jnkns_obj.create_jnkns_cron_job("revo/cron", host_name, mycommand, param)


# def daemon_get_serial_num_via_ftp():
#     #TODO: to be decided - how to pass these values to the slaves. Via jenkins is very unsafe. Hardcoded is very update unfriendly
#     FTP_SERVER_ADDRESS = "localhost"
#     FTP_USERNAME = "sid"
#     FTP_PASSWORD = "password"
#     FTP_CWD = "verizon/FTPServer"
#     FILE_NAME_STARTS_WITH = "OnlineSTBList_"

#     ftp = FTP(FTP_SERVER_ADDRESS)
#     ftp.login(user=FTP_USERNAME, passwd = FTP_PASSWORD)
#     ftp.cwd(FTP_CWD)

#     filenames = ftp.nlst() #get filenames within the directory
#     print filenames

#     try:
#         os.remove('serialnumbers.txt')
#     except OSError:
#         pass

#     def writeFunc(s):
#         localfile = open("serialnumbers.txt", 'wb')
#         localfile.write(s)

#     for filename in filenames:
#         if filename.startswith("OnlineSTBList_"):
#             metadata = ftp.sendcmd('MDTM ' + filename)
#             #print datetime.strptime(metadata[4:], "%Y%m%d%H%M%S").strftime("%d %B %Y %H:%M:%S")
#             modified_time = datetime.strptime(metadata[4:], "%Y%m%d%H%M%S")
#             elapsed_time = datetime.now() - modified_time
#             #use the data only if it was updated in the last hour, rest of the data is stale
#             if divmod(elapsed_time.total_seconds())/ (60*60) > 1: #TODO: check for timezone issues
#                 ftp.retrbinary('RETR %s' % filename, open("serialnumbers.txt", 'ab').write)

#     ftp.quit()

#     with open("serialnumbers.txt") as stb_name:
#         device_serial_num_list = stb_name.readlines()

#     logger.debug("Devices from socket: " + str(device_serial_num_list))
#     device_list = stb_devices.objects.all()
#     logger.debug("Devices from database: " + str(device_list))
#     matched_device = set([row.serial_id for row in device_list]).intersection(device_serial_num_list)
#     logger.debug("Matched Devices: " + str(matched_device))

#     sample_list = []
#     for device in device_list:
#         sample_dict = {}

#         if device.serial_id in matched_device:
#             sample_dict["STBStatus"] = 1
#         else:
#             sample_dict["STBStatus"] = 0

#         sample_dict["RouterSNo"] = device.router
#         sample_dict["STBLabel"] = device.name
#         sample_dict["STBSno"] = device.serial_id
#         sample_list.append(sample_dict)

#     jsonfile = open('app/templates/app/temp1.json', 'w')
#     out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in sample_list]) + "\n]"
#     jsonfile.write(out)


# def get_serial_num_impl():
#     print 'calling SETTOPBOX function'
#     i = 0

#     msg = \
#         'M-SEARCH * HTTP/1.1\r\n' \
#         'HOST:239.255.255.250:1900\r\n' \
#         'MX:2\r\n' \
#         'MAN:ssdp:discover\r\n' \
#         'ST:urn:schemas-upnp-org:device:ManageableDevice:2\r\n'

#     # Set up UDP socket
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     s.settimeout(5)
#     s.sendto(msg, ('239.255.255.250', 1900))

#     device_serial_num_list = []
#     count = 0
#     try:
#         while True:
#             count = count + 1
#             data, addr = s.recvfrom(65507)

#             mylist = data.split('\r')
#             url = re.findall('http?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
#             print "URL: " + url[0]
#             response = urllib2.urlopen(url[0])
#             the_page = response.read()

#             tree = ET.XML(the_page)
#             with open("temp.xml", "w") as f:
#                 f.write(ET.tostring(tree))

#             document = parse('temp.xml')
#             actors = document.getElementsByTagName("ns0:serialNumber")
#             for act in actors:
#                 for node in act.childNodes:
#                     if node.nodeType == node.TEXT_NODE:
#                         r = "{}".format(node.data)
#                         device_serial_num_list.append(str(r))
#                         i += 1
#     except socket.timeout:
#         print "I was in the except block!"
#         pass

#     device_serial_num_list = ["M11543TH4292", "M11543TH4258", "M11509TD9937"]
#     logger.debug("Devices from socket: " + str(device_serial_num_list))
#     device_list = stb_devices.objects.all()
#     logger.debug("Devices from database: " + str(device_list))
#     matched_device = set([row.unit_address for row in device_list]).intersection(device_serial_num_list)
#     logger.debug("Matched Devices: " + str(matched_device))

#     j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
#     running_builds = j.get_running_builds()
#     running_builds_path = [ urlparse(build['url']).path for build in running_builds if REVO_FOLDER_PATH in build['url']]
    
#     sample_list = []
#     for device in device_list:
#         sample_dict = {}

#         if device.unit_address in matched_device:
#             full_path = REVO_FOLDER_PATH + device.name
#             if any( path.startswith(full_path) for path in running_builds_path):
#                 sample_dict["STBStatus"] = 2
#             else:
#                 sample_dict["STBStatus"] = 1
#         else:
#             sample_dict["STBStatus"] = 0

#         sample_dict["Env"] = device.environment.name
#         sample_dict["STBLabel"] = device.name
#         sample_dict["UnitAdd"] = device.unit_address
#         sample_list.append(sample_dict)

#     jsonfile = open('app/templates/app/temp1.json', 'w')
#     out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in sample_list]) + "\n]"
#     jsonfile.write(out)


def GetSerialNum(request):
    assert isinstance(request, HttpRequest)
    # if request.method == 'GET':
        # get_serial_num_impl()
        # createActiveSTBList()
    
    return render(
        request,
        "revo/JSON/STBStatus.json",
        RequestContext(request, {
        })
    )


def createJsonFile(fileName):
    f = open(fileName, 'r')
    jsonfile = open('app/templates/app/JobStatusFile.json', 'w')
    reader = csv.DictReader(f, fieldnames=("jobNum","suiteName", "buildNum", "result", "startTime", "endTime", "duration"))
    out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in reader]) + "\n]"
    jsonfile.write(out)


def getJobStatus(request):
    assert isinstance(request, HttpRequest)
    logger.debug("Start")
    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    
    job_status_keys = ["jobNum","suiteName", "buildNum", "result", "startTime", "endTime", "duration", "userName"]
    job_status_json_file = open('app/templates/app/JobStatusFile.json', 'w')
    job_status_json_file.write("[\n\t")
    first_entry = True

    job_list = [x for x in j.get_all_jobs() if REVO_FOLDER_PATH in x['url']]    
    for job in job_list :
        job_name = job[u'fullname']
        logger.debug("Job Name: " + job_name)
        job_info = j.get_job_info(job_name)
        logger.debug("Number of builds: " + str(len(job_info[u'builds'])) + "  Job Name: " + job_name)
        
        for job_build_info in job_info[u'builds']:
            build_num = job_build_info[u'number']
            logger.debug('Job: ' + str(job_name) + ' Build # ' + str(build_num))
            
            build_info = j.get_build_info(job_name, build_num)
            try:
                 test_suite = build_info[u'actions'][0][u'parameters'][0][u'value']
            except:
                continue
            try:
                userName = build_info[u'actions'][0][u'parameters'][1][u'value']
            except:
                continue

            Duration = '...'
            current_build_number = build_num
            if str(build_info['result']) == 'None':
                status = "IN PROGRESS"
                start_time = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(((int(build_info['timestamp'])) - 18000000) / 1000))
                end_time = '---------'
            else:
                status = build_info['result']
                start_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(((int(build_info['timestamp'])) - 18000000) / 1000))
                end_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(((int(build_info['timestamp']) + int(build_info['duration']) - 18000000) / 1000)))
                Duration= int(build_info['duration'])/1000
            
            job_status_vals = [str(job_name).split('/')[1], str(test_suite), str(current_build_number), str(status), start_time, end_time, str(Duration), str(userName)]
            logger.debug("job_status_vals: " + str(job_status_vals))
            job_status_dict = dict(zip(job_status_keys, job_status_vals))
            if not first_entry:
                job_status_json_file.write(",\n\t")
            else:
                first_entry = False
            job_status_json_file.write(json.dumps(job_status_dict))

            
    queue_info = [x for x in j.get_queue_info() if REVO_FOLDER_PATH in x[u'task'][u'url']]
    for queue in queue_info:
        job_name = queue[u'task'][u'name']
        logger.debug("Job Name: " + job_name)
        current_build_number = queue[u'id']
        if "parameters" not in queue[u'actions'][0]:
            continue

        test_suite = queue[u'actions'][0][u'parameters'][0][u'value']
        userName = queue[u'actions'][0][u'parameters'][1][u'value']
        start_time = '...'
        end_time = '...'
        Duration = '...'
        status = 'IN QUEUE'
        
        job_status_vals = [str(job_name), str(test_suite), str(current_build_number), str(status), start_time, end_time, str(Duration), str(userName)]
        logger.debug("job_status_vals: " + str(job_status_vals))
        job_status_dict = dict(zip(job_status_keys, job_status_vals))
        if not first_entry:
            job_status_json_file.write(",\n\t")
        else:
            first_entry = False
        job_status_json_file.write(json.dumps(job_status_dict))
        first_entry = False
        
    job_status_json_file.write("\n]")
    job_status_json_file.close()
    
    logger.debug("End")
    return render(
        request,
        "app/JobStatusFile.json",
        {}
    )


def get_full_job_name(job_name):
    return REVO_FOLDER_NAME + '/' + job_name


def stop_job_impl(jnkns_srvr, my_job, my_build):
    logger.debug("my_job: " + my_job + "  my_build: " + str(my_build))
    try:
        if my_build in [job['id'] for job in jnkns_srvr.get_queue_info()]:
            jnkns_srvr.cancel_queue(my_build)
            logger.debug("CANCELLED QUEUE: " + "my_job: " + my_job + "  my_build: " + str(my_build))
        else:
            running_build_number = [ build['number'] for build in jnkns_srvr.get_running_builds() if REVO_FOLDER_PATH + my_job in urllib.unquote(build['url']) ]
            if running_build_number :
                jnkns_srvr.stop_build(get_full_job_name(my_job), running_build_number[0])
                logger.debug("CANCELLED BUILD: " + "my_job: " + my_job + "  my_build: " + str(my_build))
            else:
                logger.debug("JOB NEITHER IN QUEUE NOR RUNNING:  " + "my_job: " + my_job + "  my_build: " + str(my_build))
    except jenkins.NotFoundException:
        logger.error("NotFoundException + " + str(my_build))


def stopJob(request):
    assert isinstance(request, HttpRequest)
    params = json.loads(request.body)
    
    jnkns_srvr = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    if(params['job'] and params['build']):
        stop_job_impl(jnkns_srvr, params['job'], int(params['build']))
    
    return HttpResponse(json.dumps({"done" : True }), content_type='application/json')


def StopMultipleJobs(request):
    assert isinstance(request, HttpRequest)

    my_stb = request.POST.getlist('builds')
    logger.debug("my_stb: " + str(my_stb))
    loop_counter = len(my_stb) - 1
    jnkns_srvr = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    
    while loop_counter >= 0:
        x = str(my_stb[loop_counter])
        my_job = x.split(",")[0]
        my_build = int(x.split(",")[1])
        stop_job_impl(jnkns_srvr, my_job, my_build)
        loop_counter -= 1

    return HttpResponseRedirect("/revo")


from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class TestSuiteCreate(CreateView):
    model = TestSuite
    fields = '__all__'

class TestSuiteUpdate(UpdateView):
    model = TestSuite
    fields = '__all__'

class TestSuiteList(ListView):
    model = TestSuite
    context_object_name = 'test_suites'

def delete_test_suite(request) :
    assert isinstance(request, HttpRequest)
    TestSuite.objects.filter(id__in=request.POST.getlist('suite')).delete()
    return HttpResponseRedirect(reverse("test_suite_list"))


class ConfigList(ListView):
    model = Config
    context_object_name = 'configs'

class ConfigCreate(CreateView):
    model = Config
    fields = '__all__'

class ConfigUpdate(UpdateView):
    model = Config
    fields = '__all__'

def delete_config(request) :
    assert isinstance(request, HttpRequest)
    Config.objects.filter(id__in=request.POST.getlist('config')).delete()
    return HttpResponseRedirect(reverse("config_list"))


class TestCaseList(ListView):
    model = TestCase
    context_object_name = 'test_cases'

class TestCaseCreate(CreateView):
    model = TestCase
    fields = '__all__'

class TestCaseUpdate(UpdateView):
    model = TestCase
    fields = '__all__'

def delete_test_case(request) :
    assert isinstance(request, HttpRequest)
    TestCase.objects.filter(id__in=request.POST.getlist('test_case')).delete()
    return HttpResponseRedirect(reverse("test_case_list"))


class DeviceList(ListView):
    model = stb_devices
    context_object_name = 'stb_devices'

class DeviceCreate(CreateView):
    model = stb_devices
    fields = '__all__'

class DeviceUpdate(UpdateView):
    model = stb_devices
    fields = '__all__'

def delete_device(request) :
    assert isinstance(request, HttpRequest)
    stb_devices.objects.filter(id__in=request.POST.getlist('device')).delete()
    # get_serial_num_impl()
    return HttpResponseRedirect(reverse("device_list"))


def test_suite_cases(request):
    assert isinstance(request, HttpRequest)

    resp = {}
    test_suites = TestSuite.objects.all()
    for suite in test_suites:
        cases = [ case.name for case in suite.cases.all() ]
        resp[suite.name] = cases

    data = json.dumps(resp)            
    return HttpResponse(data, content_type='application/json')
