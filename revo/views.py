from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext

from app.forms import UserForm, NameForm, BootstrapAuthenticationForm
from app.models import Storm, Appium, Revo, Set_Top_Box, racktestresult
from django.contrib.auth.decorators import login_required
import jenkins
import urllib2
import urllib
import json

@login_required
def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        "revo/revo.html",
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
