from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.db.models import Sum, Avg, Count
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from app.forms import UserForm, BootstrapAuthenticationForm
from app.models import Storm, Appium, racktestresult
from revo.models import testsuite
from revo.models import device as stb_devices
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse
from django.core.exceptions import ValidationError
from ftplib import FTP
from app.jenkinsapp import JenkinsApp
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
    test_suite_list = [suite.name for suite in testsuite.objects.all()]

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
    

def create_groovy_job(job_name, wait_in_sec, **params):
  job = {}
  job["name"] = job_name
  job["WaitFor"] = wait_in_sec
  parameters = { "param1" : params.get("param1") , "param2" : params.get("param2") }
  job["Parameters"] = parameters
  return job

def schedule_job(jobs_as_json_str):
    jserver = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    
    with open('schedule.groovy', 'r') as content_file:
        content = content_file.read()

    content = "def jobsToRunStr = '" + jobs_as_json_str + "'\n" + content
    info = jserver.run_script(content)
    logger.debug("Groovy Script Info: " + info)

def sample_groovy():
    jobsToRun = []
    jobsToRun.append(create_groovy_job('IPC2_01', 10, param1="some long param", param2="def"))
    jobsToRun.append(create_groovy_job('IPC2_02', 6, param1="ac", param2="df"))
    jstr = json.dumps(jobsToRun)
    schedule_job(jstr)

########################
## Start: Revo Views  ##
########################
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
 
########################
## End: Revo Views  ##
########################
def create_jnkns_cron_job(host_name):
    jnkns_obj = JenkinsApp('http://localhost:8080', 'jenkins', 'jenkins123')
    with open("revo_configs.txt") as revo_config:
        content = revo_config.read().splitlines()
    
    test_runner_path = content[1]
    report_location = content[2]
    run_path = content[3]
    json_path = content[4]
    
    mycommand = "cd " + run_path + "\n" + "python test_stb.py " + "%param1%" + "%param2"
    jnkns_obj.create_jnkns_cron_job("revo/cron", host_name, mycommand, host_name, "ftplocation")

     

def daemon_get_serial_num_via_ftp():
    #TODO: to be decided - how to pass these values to the slaves. Via jenkins is very unsafe. Hardcoded is very update unfriendly
    ftp = FTP('FTP SERVER ADDRESS') 
    ftp.login(user='username', passwd = 'password')
    ftp.cwd("PATH ON FTP SERVER")

    filenames = ftp.nlst() # get filenames within the directory
    print filenames

    try:
        os.remove('serialnumbers.txt')
    except OSError:
        pass

    for filename in filenames:
        localfile = open("serialnumbers.txt", 'wb')
        ftp.retrbinary('RETR ' + filename, localfile.write, 1024)

    ftp.quit()

    with open("serialnumbers.txt") as stb_name:
        device_serial_num_list = stb_name.readlines()

    logger.debug("Devices from socket: " + str(device_serial_num_list))
    device_list = stb_devices.objects.all()
    logger.debug("Devices from database: " + str(device_list))
    matched_device = set([row.serial_id for row in device_list]).intersection(device_serial_num_list)
    logger.debug("Matched Devices: " + str(matched_device))

    sample_list = []
    for device in device_list:
        sample_dict = {}

        if device.serial_id in matched_device:
            sample_dict["STBStatus"] = 1
        else:
            sample_dict["STBStatus"] = 0

        sample_dict["RouterSNo"] = device.router
        sample_dict["STBLabel"] = device.name
        sample_dict["STBSno"] = device.serial_id
        sample_list.append(sample_dict)

    jsonfile = open('app/templates/app/temp1.json', 'w')
    out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in sample_list]) + "\n]"
    jsonfile.write(out)


def get_serial_num_impl():
    print 'calling SETTOPBOX function'
    i = 0

    msg = \
        'M-SEARCH * HTTP/1.1\r\n' \
        'HOST:239.255.255.250:1900\r\n' \
        'MX:2\r\n' \
        'MAN:ssdp:discover\r\n' \
        'ST:urn:schemas-upnp-org:device:ManageableDevice:2\r\n'

    # Set up UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.settimeout(5)
    s.sendto(msg, ('239.255.255.250', 1900))

    device_serial_num_list = []
    count = 0
    try:
        while True:
            count = count + 1
            data, addr = s.recvfrom(65507)

            mylist = data.split('\r')
            url = re.findall('http?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
            print "URL: " + url[0]
            response = urllib2.urlopen(url[0])
            the_page = response.read()

            tree = ET.XML(the_page)
            with open("temp.xml", "w") as f:
                f.write(ET.tostring(tree))

            document = parse('temp.xml')
            actors = document.getElementsByTagName("ns0:serialNumber")
            for act in actors:
                for node in act.childNodes:
                    if node.nodeType == node.TEXT_NODE:
                        r = "{}".format(node.data)
                        device_serial_num_list.append(str(r))
                        i += 1
    except socket.timeout:
        print "I was in the except block!"
        pass

    logger.debug("Devices from socket: " + str(device_serial_num_list))
    device_list = stb_devices.objects.all()
    logger.debug("Devices from database: " + str(device_list))
    matched_device = set([row.serial_id for row in device_list]).intersection(device_serial_num_list)
    logger.debug("Matched Devices: " + str(matched_device))

    sample_list = []
    for device in device_list:
        sample_dict = {}

        if device.serial_id in matched_device:
            sample_dict["STBStatus"] = 1
        else:
            sample_dict["STBStatus"] = 0

        sample_dict["RouterSNo"] = device.router
        sample_dict["STBLabel"] = device.name
        sample_dict["STBSno"] = device.serial_id
        sample_list.append(sample_dict)

    jsonfile = open('app/templates/app/temp1.json', 'w')
    out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in sample_list]) + "\n]"
    jsonfile.write(out)


def GetSerialNum(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'GET':
        get_serial_num_impl()
    return HttpResponseRedirect("/revo")


def createJsonFile(fileName):
    f = open(fileName, 'r')
    jsonfile = open('app/templates/app/JobStatusFile.json', 'w')
    reader = csv.DictReader(f, fieldnames=("Job No","Suite Name", "Build No", "Result", "StartTime", "EndTime", "Duration"))
    out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in reader]) + "\n]"
    jsonfile.write(out)


########Ashish(Start): new func to get job status##############
def getJobStatus(request):
    assert isinstance(request, HttpRequest)
    logger.debug("Start")
    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    
    ######'per_job_build_limit' defines the maximum number of build that can be displayed in for  a particular job.
    job_status_keys = ["Job No", "Suite Name", "Build No", "Result", "StartTime", "EndTime", "Duration", "UserName"]
    job_status_json_file = open('app/templates/app/JobStatusFile.json', 'w')
    job_status_json_file.write("[\n\t")
    first_entry = True

    per_job_build_limit = 2
    counter_1 = 0
    job_list = [x for x in j.get_all_jobs() if REVO_FOLDER_PATH in x['url']]
    job_list_len = len(job_list)
    logger.debug("Number of Jobs: " + str(job_list_len))

    while counter_1 < job_list_len :
        job_name = job_list[counter_1][u'fullname']
        logger.debug("Job Name: " + job_name)
        counter_1 += 1
        counter_2 = 0
        job_info = j.get_job_info(job_name)
        job_builds_count = len(job_info[u'builds'])
        logger.debug("Number of builds: " + str(job_builds_count) + "  Job Name: " + job_name)
        while (counter_2 < job_builds_count) and (counter_2 < per_job_build_limit):
            build_num = job_info[u'builds'][counter_2][u'number']
            logger.debug('Job: ' + str(job_name) + ' Build # ' + str(build_num))
            counter_2 = counter_2 + 1
            build_info = j.get_build_info(job_name, build_num)
            try:
                 test_suite = build_info[u'actions'][0][u'parameters'][0][u'value']
            except:
                test_suite = '...'
            try:
                userName = build_info[u'actions'][0][u'parameters'][1][u'value']
            except:
                userName = '...'

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
    queue_info_len = len(queue_info)
    counter_3 = 0
    logger.debug("Number of queues: " + str(queue_info_len))
    while counter_3 < queue_info_len:
        job_name = queue_info[counter_3][u'task'][u'name']
        logger.debug("Job Name: " + job_name)
        current_build_number = queue_info[counter_3][u'id']
        #TODO: Add checks there can be other jobs as well wout parameters
        test_suite = queue_info[counter_3][u'actions'][0][u'parameters'][0][u'value']
        userName = queue_info[counter_3][u'actions'][0][u'parameters'][1][u'value']
        start_time = '...'
        end_time = '...'
        Duration = '...'
        status = 'IN QUEUE'
        counter_3 = counter_3+1
        
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
    jnkns_srvr = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    stop_job_impl(jnkns_srvr, request.GET['job'], int(request.GET['build']))
    
    return render(
        request,
        "app/JobStatusFile.json",
        RequestContext(request,{ })
    )


def StopMultipleJobs(request):
    assert isinstance(request, HttpRequest)

    my_stb = request.POST.getlist('check2')
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


def Json(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/temp1.json",
        RequestContext(request, {
        })
    )

def Json2(request):
    getJobStatus(request)
    time.sleep(6)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/JobStatusFile.json",
        RequestContext(request,
        {
        })
    )


@login_required
def device_list(request):
    assert isinstance(request, HttpRequest)

    devices = [ { "name": row.name, "serial_num" : row.serial_id, "router" : row.router, "host" : row.host } for row in stb_devices.objects.all()]
    return render(
        request,
        "revo/device_list.html",
        RequestContext(request, {
         "devices" : devices
        })
    )

@login_required
def device_add_view(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "revo/device_add_view.html",
        RequestContext(request, {
         
        })
    )

def add_device(request) :
    assert isinstance(request, HttpRequest)

    new_device = stb_devices()
    new_device.name = request.POST.get('device-name')
    new_device.mac_id = request.POST.get('device-id')
    new_device.serial_id = request.POST.get('serial-id')
    new_device.device_type = request.POST.get('device-type')
    new_device.ip = request.POST.get('ip')
    new_device.router = request.POST.get('router')
    host_name = request.POST.get('host-name')
    new_device.host = host_name

    host_name_count = stb_devices.objects.filter(host=host_name).count()
    try:
        if new_device.name and new_device.serial_id and new_device.router and new_device.host:
            logger.debug("Data line1: " + request.POST.get('device-name') + " : "  + request.POST.get('serial-id'))
            logger.debug("Data line2: " + request.POST.get('device-type') + " : "  + request.POST.get('ip') + " : " + request.POST.get('device-id'))
            logger.debug("Data line3: " + request.POST.get('router') + " : "  + request.POST.get('host-name'))
            new_device.save()
            print "ADDED device name: " + request.POST.get('device-name') + "  Device Id:  " + request.POST.get('device-id')

            if host_name_count == 0 :
                create_jnkns_cron_job(host_name)
           
    except ValidationError as err:
        logger.error("ValidationError: " + str(err))
    except Exception as exception:
        logger.error("EXCEPTION: " + str(exception))
        print str(exception)

    get_serial_num_impl()
    return HttpResponseRedirect("/revo/devices/list_view")

def delete_device(request) :
    assert isinstance(request, HttpRequest)
    stb_devices.objects.filter(name__in=request.POST.getlist('device_name')).delete()
    get_serial_num_impl()
    return HttpResponseRedirect("/revo/devices/list_view")

@login_required
def configs(request):
    assert isinstance(request, HttpRequest)
    with open("revo_configs.txt") as revo_config:
        content = revo_config.readlines()
    
    return render(
        request,
        "revo/configs.html",
        RequestContext(request, {
            "loc" : content[0],
            "test_runner_path" : content[1],
            "report_location" : content[2],
            "run_path" : content[3],
            "json_path" : content[4],
        })
    )

def add_configurations(request) :
    assert isinstance(request, HttpRequest)
    loc_fix = str(request.POST.get('loc_fix'))
    test_runner_path = str(request.POST.get('test_runner_path'))
    report_location = str(request.POST.get('report_location'))
    run_path = str(request.POST.get('run_path'))
    json_path = str(request.POST.get('json_path'))
    
    if loc_fix and test_runner_path and report_location and run_path and json_path:
        print loc_fix + test_runner_path + report_location + run_path + json_path
        config_file = open("revo_configs.txt", "w")
        config_file.write(loc_fix+ "\n")
        config_file.write(test_runner_path+ "\n")
        config_file.write(report_location+ "\n")
        config_file.write(run_path+ "\n")
        config_file.write(json_path+ "\n")
        config_file.close()
    return HttpResponseRedirect("/revo/configs/")


@login_required
def test_suites_add_view(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "revo/test_suites.html",
        RequestContext(request, {
            
        })
    )

@login_required
def test_suites_list(request):
    assert isinstance(request, HttpRequest)
    suite = [ { "name": row.name, "mapping" : row.mapping_name} for row in testsuite.objects.all()]
    return render(
        request,
        "revo/test_suite_list.html",
        RequestContext(request, {
            "suite" : suite,
        })
    )


def add_test_suite(request) :
    assert isinstance(request, HttpRequest)
    names = request.POST.getlist('names')
    mappings = request.POST.getlist('mappings')

    for index in range(0, len(names)):
        if str(names[index]) and str(mappings[index]):
            test_suite = testsuite(name = str(names[index]), mapping_name = str(mappings[index]))
            test_suite.save()
            print "ADDED TEST SUITE name: " + str(names[index]) + "  mapping_name: " + str(mappings[index])

    return HttpResponseRedirect("/revo/test_suites/list_view")


def delete_test_suite(request) :
    assert isinstance(request, HttpRequest)
    testsuite.objects.filter(name__in=request.POST.getlist('tset_suite_name')).delete()
    return HttpResponseRedirect("/revo/test_suites/list_view")

from .forms import DeviceMForm

@login_required
def device(request):
    if request.method == "POST":
        form = DeviceMForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/revo/test_suites/list_view")
    else:
        form = DeviceMForm()

    return render(request, "revo/device.html" , RequestContext(request, {
            'form' : form
        }))

