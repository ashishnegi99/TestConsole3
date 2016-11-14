from django.shortcuts import render
from datetime import datetime, date, timedelta
from app.models import racktestresult
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
@login_required
def reports_home(request):
    date_from_str = None
    date_to_str = None

    if 'q1' and 'q2' in request.GET:
        date_from_str = request.GET['q1']
        date_to_str = request.GET['q2']

    today = datetime.now()    
    date_to = today if not date_from_str else datetime.strptime(date_to_str, "%Y-%m-%d") 
    date_from = date_to + timedelta(days=-90) if not date_from_str else datetime.strptime(date_from_str, "%Y-%m-%d")
    
    
    db_response = racktestresult.objects.filter(Date__range = (date_from, date_to))
    db_resp_today = racktestresult.objects.filter(Date__range = (today + timedelta(days=-1), today))
    today_pass = db_resp_today.filter(Result = "PASS").count()
    today_total = db_resp_today.count()
        
    total_pass = db_response.filter(Result = "PASS").count()
    total_fail = db_response.filter(Result = "FAIL").count()
    total_total = db_response.count()

    stripped_db_response = db_response.values_list('PassNumbers','FailNumbers', 'TestJobName', 'Date')
    pass_num = [x[0] for x in stripped_db_response]
    fail_num = [x[1] for x in stripped_db_response]
    job_name = json.dumps([x[2] for x in stripped_db_response])
    dates = [x[3].strftime('%m/%d/%Y') for x in stripped_db_response]

    date_from_str = json.dumps(str(date_from))
    date_to_str = json.dumps(str(date_to))

    return render(
        request,
        "reports/home.html",
        {
            "todayPass" : today_pass,
            "todayTotal": today_total,
            "totalPass" : total_pass,
            "totalFail" : total_fail, 
            "totalTotal": total_total,
            "passNums"  : pass_num,
            "failNums"  : fail_num,
            "jobNames"  : job_name,
            "dates"     : dates,
            "from"      : date_from_str,
            "to"        : date_to_str
        }
    )