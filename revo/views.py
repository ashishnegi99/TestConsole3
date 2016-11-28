from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.db.models import Sum, Avg, Count
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from app.forms import UserForm, NameForm, BootstrapAuthenticationForm
from app.models import Storm, Appium, Revo, Set_Top_Box, racktestresult
from revo.models import testsuite, device
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse
from django.core.exceptions import ValidationError
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
    
########################
## Start: Revo Views  ##
########################
def revo_view(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
    else:
        form = NameForm()
    
    cd1 = "<command>"
    cd2 = "</command>"
    mycommand2 = cd1 + "import time"+"\n" + "time.sleep(500)" + cd2
    new_job_config = "<?xml version='1.0' encoding='UTF-8'?><project><actions/><description></description><keepDependencies>false</keepDependencies><properties><hudson.model.ParametersDefinitionProperty><parameterDefinitions><hudson.model.StringParameterDefinition><name>param1</name><description></description><defaultValue></defaultValue></hudson.model.StringParameterDefinition><hudson.model.StringParameterDefinition><name>param2</name><description></description><defaultValue></defaultValue></hudson.model.StringParameterDefinition></parameterDefinitions></hudson.model.ParametersDefinitionProperty></properties><scm class='hudson.scm.NullSCM'/><canRoam>true</canRoam><disabled>false</disabled><blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding><blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding><triggers/><concurrentBuild>false</concurrentBuild><builders><hudson.tasks.BatchFile><command>timeout 500</command></hudson.tasks.BatchFile></builders><publishers/><buildWrappers/></project>"
    
    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')

    new_folder_config = '<com.cloudbees.hudson.plugins.folder.Folder plugin="cloudbees-folder@5.13"><actions/><description/><displayName>revo</displayName><properties/><views><hudson.model.AllView><owner class="com.cloudbees.hudson.plugins.folder.Folder" reference="../../.."/><name>All</name><filterExecutors>false</filterExecutors><filterQueue>false</filterQueue><properties class="hudson.model.View$PropertyList"/></hudson.model.AllView></views><viewsTabBar class="hudson.views.DefaultViewsTabBar"/><healthMetrics><com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric/></healthMetrics><icon class="com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon"/></com.cloudbees.hudson.plugins.folder.Folder>'
    new_view_config = '<hudson.model.ListView><name>revo_view</name><filterExecutors>false</filterExecutors><filterQueue>false</filterQueue><properties class="hudson.model.View$PropertyList"/><jobNames><comparator class="hudson.util.CaseInsensitiveComparator"/><string>revo</string></jobNames><jobFilters/><columns><hudson.views.StatusColumn/><hudson.views.WeatherColumn/><hudson.views.JobColumn/><hudson.views.LastSuccessColumn/><hudson.views.LastFailureColumn/><hudson.views.LastDurationColumn/><hudson.views.BuildButtonColumn/></columns><recurse>false</recurse></hudson.model.ListView>'

    if j.job_exists('revo') != True:
        j.create_job('revo', new_folder_config)

    # if j.view_exists("revo_view") != True:
    #     j.create_view("revo_view", new_view_config)

    form = NameForm(request.POST)
    my_stb = request.POST.getlist('check1')
    my_test_suite = request.POST.getlist('checks')
    user_name = request.user.username
    count1 = 0
    for s in my_stb:
        count2 = 0
        for t in my_test_suite:
            job_path = "revo/" + my_stb[count1]
            print job_path, ' : ', my_test_suite[count2]
            
            if not j.job_exists(job_path):
                j.create_job(job_path, new_job_config)
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
                j.reconfig_job(job_path, shellCommand)
                j.build_job(job_path,{'param1': my_test_suite[count2],'param2': user_name})
                        
            else:
                j.enable_job(job_path)
                jobConfig = j.get_job_config(job_path)
                print "Before RECONFIG"
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
                j.reconfig_job(job_path, shellCommand)
                
                print "RECONFIG"
                j.build_job(job_path,{'param1': my_test_suite[count2],'param2': user_name})
                count2 = count2+1    
        count1 = count1+1
 
    return HttpResponseRedirect("/revo")
 
########################
## End: Revo Views  ##
########################

def logToJobFile(abc):
    logFile = open("CreatedJobsFile.csv", "a+")
    logFile.write(abc + "\n")



def GetSerialNum(request):
    if request.method == 'GET':

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

        try:
            os.remove('serialnumbers.txt')
        except OSError:
            pass

        def logToFile(logTxt):
            logFile = open("serialnumbers.txt", "a+")
            logFile.write(logTxt + "\n")
            # print logTxt

        count = 0
        try:
            while True:
                count = count + 1
                data, addr = s.recvfrom(65507)

                mylist = data.split('\r')
                url = re.findall('http?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
                print url[0]
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
                            print r
                            logToFile(str(r))
                            i += 1
                            print i

        except socket.timeout:
            print "I WAs in the except block"
            pass

        f = open("Reference_File.txt", "r")
        reader = csv.reader(f)

        data = open("temp1.csv", "wb")
        w = csv.writer(data)
        for row in reader:
            my_row = []
            my_row.append(row[0])
            w.writerow(my_row)
        data.close()

        with io.open('temp1.csv', 'r') as file1:
            with io.open('serialnumbers.txt', 'r') as file2:
                same = set(file1).intersection(file2)
                print same

        with open('results.csv', 'w') as file_out:
            for line in same:
                file_out.write(line)
                print line

        with open('results.csv', 'rb') as f:
            reader = csv.reader(f)
            result_list = []
            for row in reader:
                result_list.extend(row)

        with open('Reference_File.txt', 'rb') as f:
            reader = csv.reader(f)
            sample_list = []
            for row in reader:
                if row[0] in result_list:
                    sample_list.append(row + [1])
                else:
                    sample_list.append(row + [0])

        with open('sample_output.csv', 'wb') as f:
            writer = csv.writer(f)
            writer.writerows(sample_list)
            print

        f = open('sample_output.csv', 'r')
        jsonfile = open('app/templates/app/temp1.json', 'w')
        reader = csv.DictReader(f, fieldnames=("STBSno", "STBLabel", "RouterSNo", "STBStatus"))
        out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in reader]) + "\n]"
        jsonfile.write(out)
    assert isinstance(request, HttpRequest)
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

def add_test_suite(request) :
    assert isinstance(request, HttpRequest)
    names = request.POST.getlist('names')
    mappings = request.POST.getlist('mappings')

    for index in range(0, len(names)):
        if str(names[index]) and str(mappings[index]):
            test_suite = testsuite(name = str(names[index]), mapping_name = str(mappings[index]))
            test_suite.save()
            print "ADDED TEST SUITE name: " + str(names[index]) + "  mapping_name: " + str(mappings[index])

    return HttpResponseRedirect("/test_suites")


def add_device(request) :
    assert isinstance(request, HttpRequest)

    # if request.POST.get('device-name') and request.POST.get('device-id') :
    new_device = device()
    new_device.name = request.POST.get('device-name')
    new_device.mac_id = request.POST.get('device-id')
    new_device.serial_id = request.POST.get('serial-id')
    new_device.device_type = request.POST.get('device-type')
    new_device.ip = request.POST.get('ip')
    new_device.router = request.POST.get('router')
    try:
        new_device.save()
        print "ADDED device name: " + request.POST.get('device-name') + "  Device Id:  " + request.POST.get('device-id')
    except ValidationError as err:
        logger.error("ValidationError: " + str(err))
    except Exception as exception:
        logger.error("Data line1: " + request.POST.get('device-name') + request.POST.get('device-id') + request.POST.get('serial-id'))
        logger.error("Data line2: " + request.POST.get('device-type') + request.POST.get('ip') + request.POST.get('router'))
        logger.error("EXCEPTION: " + str(exception))
        print str(exception)

    return HttpResponseRedirect("/device")