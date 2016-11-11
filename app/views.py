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
        "app/layout.html",
        RequestContext(request, {
            "title":"Home Page",
        })
    )
    
@login_required
def revohtml(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "app/revo.html",
        RequestContext(request, {
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
    print request.POST.getlist('checks')
    print request.POST.getlist('optradio')

    form = NameForm(request.POST)
    stb1 = request.POST.getlist('optradio')
    list1 = request.POST.getlist('checks')
    cd1 = "<command>"
    cd2 = "</command>"
    test_runner_path2 = "cd C:\git_new\evo_automation\ tests\TestRunner"
    # request.POST.getlist('check1')

    STB = ', '.join(stb1)

    TestSuite = ', '.join(list1)
    # TestSuite1 = "REG_AGREED_SUITE02"
    report_location = "C:\git_new\evo_automation\ tests\TestRunner\ReportFile C:\git_new\evo_automation\ reports"

    # mycommand2 = cd1 + test_runner_path2 + "\n" + STB + "\n" + TestSuite + "\nTrue \n" + report_location + cd2
    mycommand2 = cd1 + "import time"+"\n" + "time.sleep(500)" + cd2
    print "mycommand2", mycommand2

    myNewJob = STB
    myXML = "<?xml version='1.0' encoding='UTF-8'?><project><actions/><description></description><keepDependencies>false</keepDependencies><properties/><scm class='hudson.scm.NullSCM'/><canRoam>true</canRoam><disabled>false</disabled><blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding><blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding><triggers/><concurrentBuild>false</concurrentBuild><builders><hudson.plugins.python.Python plugin='python@1.3'><command>RawComamnd</command></hudson.plugins.python.Python></builders><publishers/><buildWrappers/></project>"

    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')

    if not j.job_exists(myNewJob):
        j.create_job(myNewJob, myXML)
        j.enable_job(myNewJob)
        jobConfig = j.get_job_config(myNewJob)
        ###### print "Before RECONFIG"
        ###### print j.get_job_config(myNewJob)

        ######Start: to retrieve previous command######
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
        ######End: to retrieve previous command######

        shellCommand = jobConfig.replace(prev_command, mycommand2)
        j.reconfig_job(myNewJob, shellCommand)

        ###### print "RECONFIG"
        ###### print j.get_job_config(myNewJob)

        j.build_job(myNewJob)

        # #####  Start: code to get job status   ######
        current_build_number = j.get_job_info(myNewJob)['nextBuildNumber']
        print "Current Build Number : ", current_build_number
        print "Job Building In Progress -"
        time.sleep(15)
        build_info = j.get_build_info(myNewJob, current_build_number)

        if str(build_info['result']) == 'SUCCESS':
            print"+++++    BUILD COMPLETED"
            print build_info['displayName']
        elif str(build_info['result']) == 'FAILURE':
            print"XXXXX    BUILD FAILED"
            print build_info['displayName']
        elif str(build_info['result']) == 'None':
            print"......   JOB IN PROGRESS"
            print build_info['displayName']
        else:
            print "HOLA"
            print build_info['displayName']
        #####  End: code to get job status   ######

        #####  Start: code to get Job Start Time   ######
        startTime1 = str(build_info['timestamp'])
        # print startTime1
        ####reduce the time by 5 hrs as tfhe jenkin time is coming 5 hrs extra##########
        startTime1 = int(startTime1) - 18000000
        startTime2 = float(startTime1) / 1000
        # print (startTime2)
        # print time.gmtime(startTime2)
        print time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(startTime2))


    else:
        j.enable_job(myNewJob)
        jobConfig = j.get_job_config(myNewJob)
        print "Before RECONFIG"
        print j.get_job_config(myNewJob)
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
        j.reconfig_job(myNewJob, shellCommand)

        print "RECONFIG"
        print j.get_job_config(myNewJob)

        j.build_job(myNewJob)

        # #####  Start: code to get job status   ######
        current_build_number = j.get_job_info(myNewJob)['nextBuildNumber']
        print "Current Build Number : ", current_build_number

        prv_build_number = j.get_job_info(myNewJob)['lastBuild']['number']
        print "Last Build Number :", prv_build_number

        i = 0
        while (i < 6) and (current_build_number != prv_build_number):
            print "Status In Progress -", i
            time.sleep(2)
            i = i + 1
            prv_build_number = j.get_job_info('sample')['lastBuild']['number']
        else:
            print "Job completed -", current_build_number

        try:

            build_info = j.get_build_info(myNewJob, current_build_number)
            startTime1 = str(build_info['timestamp'])
            # print startTime1
            ####reduce the time by 5 hrs as tfhe jenkin time is coming 5 hrs extra##########
            startTime1 = int(startTime1) - 18000000
            startTime2 = float(startTime1) / 1000
            # print (startTime2)
            # print time.gmtime(startTime2)
            print time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(startTime2))
            #####  Start: code to get Job Start Time   ######
            if str(build_info['result']) == 'SUCCESS':
                print"+++++    BUILD COMPLETED"
                status = "JOB COMPLETED"
                print build_info['displayName']
            elif str(build_info['result']) == 'FAILURE':
                print"XXXXX    BUILD FAILED"
                status = "JOB FAILED"
                print build_info['displayName']
            elif str(build_info['result']) == 'None':
                print"......   JOB IN PROGRESS"
                status = "JOB IN PROGRESS"
                print build_info['displayName']
            else:
                print "HOLA"
                print build_info['displayName']
        except jenkins.NotFoundException:

            print "......JOB IN QUEUE"
            status = "JOB IN QUEUE"
            startTime2 = 000000
            pass
        #####  End: code to get job status   ######

        #####  Start: code to get Job Start Time   ######


        logToJobFile(str(STB)+","+str(TestSuite)+","+str(current_build_number)+","+str(status)+","+time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(startTime2)))

        return HttpResponseRedirect("home")

    # return render(request, 'app/revo.html', {'form': form})

        return render(
        request,
        "revo.html",
        {
            
        }
    )
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
        "app/layout.html",
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
    import csv
    import jenkins
    import urllib2
    import urllib
    import sys
    import json
    import ast
    import time

    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')

    f = open("CreatedJobsFile.csv", "r")
    m = open("JobStatusFile.csv", "w")
    reader = csv.reader(f)
    writer = csv.writer(m)
    for row in reader:
        try:
            build_info = j.get_build_info(str(row[0]), int(row[2]))
            StartTime = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(((int(build_info['timestamp'])) - 18000000) / 1000))

            if str(build_info['result']) == 'None':
                result = "IN PROGRESS"
                EndTime = "-------"
                Duration = "-------"
            else:
                result = build_info['result']
                EndTime = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(((int(build_info['timestamp'])+int(build_info['duration'])-18000000)/1000)))
                Duration= int(build_info['duration'])/1000
        except jenkins.NotFoundException:
            result = "JOB IN QUEUE"
            pass

        # print row[0], row[1],row[2], result, StartTime, EndTime, str(Duration)
        m.write(row[0] + "," + row[1] + ","+row[2]+","+ result + "," + StartTime + "," + EndTime + "," + str(Duration) + " Secs" + "\n")

    f.close()
    m.close()
    createJsonFile("JobStatusFile.csv")

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
    print "KILL BILL"
    # print "a:",request
    # print "Method:", request.method
    # print "Method:", request.GET
    print "***Job***", request.GET['job']
    print "***Build***", request.GET['build']
    # < WSGIRequest: GET '/stopJob?name=STB+1&time=9' >
    # print printgetattr(request.job);
    j = jenkins.Jenkins('http://localhost:8080', 'jenkins', 'jenkins123')
    j.stop_build(request.GET['job'],request.GET['build'])
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
        "app/layout.html",
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
        "app/layout.html",
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



def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            registered = True

        else:
            pass
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(
            'app/user/register_form.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)