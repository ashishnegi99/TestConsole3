from datetime import datetime
from django.conf.urls import patterns, include, url
from app.forms import BootstrapAuthenticationForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    
##User Stuff
    url(r"^user/login/$",
        "django.contrib.auth.views.login",
        {
            "template_name": "app/login.html",
            "authentication_form": BootstrapAuthenticationForm,
            "extra_context":
            {
                "title":"Log in",
                "year":datetime.now().year,
            }
        },
        name="login"),
    url(r"^logout$",
        "django.contrib.auth.views.logout",
        {
            "next_page": "/",
        },
        name="logout"),

##Test Console
    url(r"^home", "testconsole.views.home", name="home"),
    url(r"^$", "testconsole.views.home", name="home"),

## StopMultipleJobs's
    url(r"^StopMultipleJobs", "testconsole.views.StopMultipleJobs", name="StopMultipleJobs"),

## JobStatus's
    url(r"^JobStatus", "testconsole.views.getJobStatus", name="JobStatus"),

## StopStatus's
    url(r"^stopJob", "testconsole.views.stopJob", name="stopJob"),



## Revo's
    url(r"^Revo", "testconsole.views.Revo_view", name="Revo"),

## Appium's
    url(r"^Appium", "testconsole.views.Appium", name="Appium"),
	
## Storm's
    url(r"^Storm", "testconsole.views.Storm", name="Storm"),

## Json's
    url(r"^Json", "testconsole.views.Json", name="Json"),

## Json2's
    url(r"^Json2", "testconsole.views.Json2", name="Json2"),

#SetTopBox
    url(r"^Set_Top_Box", "testconsole.views.GetSerialNum", name="Set_Top_Box"),




## Reports
    url(r"^Reports", "reports.views.reports_home", name="Reports"),

## Report's
    url(r"^ReportsLink", "testconsole.views.reportslink", name="ReportsLink"),

##Admin
    url(r"^admin/", include(admin.site.urls)),

)