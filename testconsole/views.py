# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime, date, timedelta
from app.forms import UserForm, NameForm, BootstrapAuthenticationForm
from app.models import Storm, Appium, Revo, Set_Top_Box, racktestresult
from django.contrib.auth.decorators import login_required
import jenkins
import urllib2
import urllib
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse
import socket
import time
import string
import re
from xml.etree import ElementTree as ET
from xml.dom.minidom import parse
import os
import io
import csv
import json
import json as simplejson
from django.db.models import Avg
from django.db.models import Sum, Avg, Count
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect


@login_required
def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "testconsole/layout.html",
        RequestContext(request,
        {
            "title":"Home Page",
        })
    )


def reportslink(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "testconsole/index.html",
        RequestContext(request,
        {
        })
    )	
	
########################
## Start: Revo Views  ##
########################
def Revo_view(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
    else:
        form = NameForm()
    print request.POST.getlist('check1')
    print request.POST.getlist('checks')
	###start: passing username
	# if request.method == 'POST':
        # form = BootstrapAuthenticationForm(request.POST)
    # else:
        # form = BootstrapAuthenticationForm()

    # username = request.POST.getlist('username')
    # print username
	###end: passing username	
    cd1 = "<command>"
    cd2 = "</command>"
    test_runner_path2 = "cd C:\git_new\evo_automation\ tests\TestRunner"
    report_location = "C:\git_new\evo_automation\ tests\TestRunner\ReportFile C:\git_new\evo_automation\ reports"
    mycommand2 = cd1 + "import time"+"\n" + "time.sleep(500)" + cd2
    myXML_1 = "<?xml version='1.0' encoding='UTF-8'?><project><actions/><description></description><keepDependencies>false</keepDependencies><properties><hudson.model.ParametersDefinitionProperty><parameterDefinitions><hudson.model.StringParameterDefinition><name>param1</name><description></description><defaultValue></defaultValue></hudson.model.StringParameterDefinition><hudson.model.StringParameterDefinition><name>param2</name><description></description><defaultValue></defaultValue></hudson.model.StringParameterDefinition></parameterDefinitions></hudson.model.ParametersDefinitionProperty></properties><scm class='hudson.scm.NullSCM'/><canRoam>true</canRoam><disabled>false</disabled><blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding><blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding><triggers/><concurrentBuild>false</concurrentBuild><builders><hudson.plugins.python.Python plugin='python@1.3'><command>i am a new job</command></hudson.plugins.python.Python></builders><publishers/><buildWrappers/></project>"
    myXML = "<?xml version='1.0' encoding='UTF-8'?><project><actions/><description></description><keepDependencies>false</keepDependencies><properties/><scm class='hudson.scm.NullSCM'/><canRoam>true</canRoam><disabled>false</disabled><blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding><blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding><triggers/><concurrentBuild>false</concurrentBuild><builders><hudson.plugins.python.Python plugin='python@1.3'><command>RawComamnd</command></hudson.plugins.python.Python></builders><publishers/><buildWrappers/></project>"
    
    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')

    form = NameForm(request.POST)
    my_stb = request.POST.getlist('check1')
    my_test_suite = request.POST.getlist('checks')
    count1 = 0
    for s in my_stb:
        count2 = 0
        for t in my_test_suite:
            print my_stb[count1], ' : ', my_test_suite[count2]
            
            if not j.job_exists(my_stb[count1]):
                j.create_job(my_stb[count1], myXML_1)
                j.enable_job(my_stb[count1])
                jobConfig = j.get_job_config(my_stb[count1])
       
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
                j.reconfig_job(my_stb[count1], shellCommand)
                j.build_job(my_stb[count1],{'param1': my_test_suite[count2]})
                        
            else:
                j.enable_job(my_stb[count1])
                jobConfig = j.get_job_config(my_stb[count1])
                print "Before RECONFIG"
#                 print j.get_job_config(my_stb[count1])
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
                j.reconfig_job(my_stb[count1], shellCommand)
                
                print "RECONFIG"
#                 print j.get_job_config(my_stb[count1])
                j.build_job(my_stb[count1],{'param1': my_test_suite[count2]})
                count2 = count2+1    
#                 j.build_job(name, parameters, token)        
        count1 = count1+1
  
 
    return HttpResponseRedirect("home")
 
    return render(request, 'testconsole/layout.html', {'form': form})
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
    return render(
        request,
        "testconsole/layout.html",
        RequestContext(request,
        {
            "title":"Revo",
            "message":"Stuff about revo goes here.",
            "year":datetime.now().year,
        })
    )

def createJsonFile(fileName):
    f = open(fileName, 'r')
    jsonfile = open('app/templates/app/JobStatusFile.json', 'w')
    reader = csv.DictReader(f, fieldnames=("Job No","Suite Name", "Build No", "Result", "StartTime", "EndTime", "Duration"))
    out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in reader]) + "\n]"
    jsonfile.write(out)


########Ashish(Start): new func to get job status##############
def getJobStatus(request):
    import jenkins
    import time
    import csv
    import json
    
    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    file_name = "JobStatusFile.csv"
    m = open(file_name, "w")
    ######'per_job_build_limit' defines the maximum number of build that can be displayed in
    ######for  a particular job.
    per_job_build_limit = 2
    counter_1 = 0
    print j.get_all_jobs()
    while counter_1 < j.get_all_jobs().__len__():
        job_name = j.get_all_jobs()[counter_1][u'name']
        print "Job Name: ", job_name
        counter_1 = counter_1 + 1
        counter_2 = 0
        while (counter_2 < j.get_job_info(job_name)[u'builds'].__len__()) and (counter_2 < per_job_build_limit):
            build_num = j.get_job_info(job_name)[u'builds'][counter_2][u'number']
            print 'Job: ', job_name, ' Build # ', build_num
            counter_2 = counter_2 + 1
            build_info = j.get_build_info(job_name, build_num)
            STB = job_name
            try:
                 TestSuite = j.get_build_info(job_name, build_num)[u'actions'][0][u'parameters'][0][u'value']
                 print TestSuite
            except:
                TestSuite = '...'
            Duration = '...'
            current_build_number = build_num
#             if str(build_info['result']) == 'SUCCESS':
#                 print"+++++    BUILD COMPLETED"
#                 status = "JOB COMPLETED"
#                 start_time = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(((int(build_info['timestamp'])) - 18000000) / 1000))
#                 end_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(((int(build_info['timestamp']) + int(build_info['duration']) - 18000000) / 1000)))
#             elif str(build_info['result']) == 'FAILURE':
#                 print"XXXXX    BUILD FAILED"
#                 status = "JOB FAILED"
#                 start_time = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(((int(build_info['timestamp'])) - 18000000) / 1000))
#                 end_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime((int(build_info['timestamp']) + int(build_info['duration']) - 18000000) / 1000))
            if str(build_info['result']) == 'None':
                print"......   JOB IN PROGRESS"
                status = "IN PROGRESS"
                start_time = time.strftime('%m/%d/%Y %H:%M:%S',time.gmtime(((int(build_info['timestamp'])) - 18000000) / 1000))
                end_time = '---------'
            else:
                status = build_info['result']
                start_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(((int(build_info['timestamp'])) - 18000000) / 1000))
                end_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(((int(build_info['timestamp']) + int(build_info['duration']) - 18000000) / 1000)))
                Duration= int(build_info['duration'])/1000
#             else:
#                 print "HOLA"
#                 status = "HOLA"
#                 print build_info['displayName']
#                 start_time = '---------'
#                 end_time = '---------'
                
#                 start_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(((int(build_info['timestamp'])) - 18000000) / 1000))
#                 end_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(((int(build_info['timestamp']) + int(build_info['duration']) - 18000000) / 1000)))
            abc = (str(STB) + "," + str(TestSuite) + "," + str(current_build_number) + "," + str(status) + "," + start_time + "," + end_time + "," + str(Duration))
#             if start_time < str(date.today()):
            m.write(abc + "\n")
    
    
    a = j.get_queue_info()
    if  a.__len__()>0:
        print 'No queue'
        counter_3 = 0
        while counter_3 < j.get_queue_info().__len__():
            STB = a[counter_3][u'task'][u'name']
            print 'Job: ', a[counter_3][u'task'][u'name']
            current_build_number = a[counter_3][u'id']
            print 'id/current_build_number: ', a[counter_3][u'id']
            TestSuite = a[counter_3][u'actions'][0][u'parameters'][0][u'value']
            print 'test suite: ', a[counter_3][u'actions'][0][u'parameters'][0][u'value']
            start_time = '...'
            end_time = '...'
            Duration = '...'
            print 'start and end time: ', '...'
            status = 'IN QUEUE'
            counter_3 = counter_3+1
            
            abc = (str(STB) + "," + str(TestSuite) + "," + str(current_build_number) + "," + str(status) + "," + start_time + "," + end_time + "," + str(Duration))
#             if start_time < str(date.today()):
            m.write(abc + "\n")
    
    
    m.close()
    f = open(file_name, 'r')
    jsonfile = open('app/templates/app/JobStatusFile.json', 'w')
    reader = csv.DictReader(f,fieldnames=("Job No", "Suite Name", "Build No", "Result", "StartTime", "EndTime", "Duration"))
    out = "[\n\t" + ",\n\t".join([json.dumps(row) for row in reader]) + "\n]"
    jsonfile.write(out)
    jsonfile.close()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/JobStatusFile.json",
        RequestContext(request,
                       {
                       })
    )

#######Ashish(End): new func to get job status##############

def stopJob(request):
    print "KILL QUEUE"
    print "***Job***", request.GET['job']
    print "***QueueID***", request.GET['build']
    
    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    
    try:
        queue_info = j.get_build_info(request.GET['job'], int(request.GET['build']))
        print "...Job is in progress: "
        j.stop_build(request.GET['job'], int(request.GET['build'])) 
    except jenkins.NotFoundException:
        print "......JOB IN QUEUE"
        j.cancel_queue(request.GET['build'])
    
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/JobStatusFile.json",
        RequestContext(request,
                       {
                       })
    )

def StopMultipleJobs(request):
    print "KILL ALL"
    form = NameForm(request.POST)
    my_stb = request.POST.getlist('check2')
    print len(my_stb)
    counter_4 =0
    while counter_4 < len(my_stb):
        print str(my_stb[counter_4])
        x = str(my_stb[counter_4])
        print x.split(",")[0]
        print x.split(",")[1]
        my_job = x.split(",")[0]
        my_build = int(x.split(",")[1])
        j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
        try:
            queue_info = j.get_build_info(my_job, my_build)
            print "...Job is in progress: "
            j.stop_build(my_job, my_build) 
        except jenkins.NotFoundException:
            print "......JOB IN QUEUE"
            j.cancel_queue(my_build)
        counter_4 = counter_4+1
    assert isinstance(request, HttpRequest)
    
    return HttpResponseRedirect("home")
 
    return render(
        request,
        "app/JobStatusFile.json",
        RequestContext(request,
                       {
                       })
    )

@login_required
def Storm(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "testconsole/layout.html",
        RequestContext(request,
        {
            "title":"Storm",
            "message":"Stuff about Storm goes here",
            "year":datetime.now().year,
        })
    )

@login_required
def Appium(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "testconsole/layout.html",
        RequestContext(request,
        {
            "title":"Appium",
            "message":"Stuff about Appium goes here.",
            "year":datetime.now().year,
        })
    )

def Json(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/temp1.json",
        RequestContext(request,
        {
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