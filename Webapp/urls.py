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
    url(r"^home", "app.views.home", name="home"),
    url(r"^$", "app.views.home", name="home"),




## Revo's
    url(r"^revo", "revo.views.home", name="revo"),
## StopMultipleJobs's
    url(r"^StopMultipleJobs", "revo.views.StopMultipleJobs", name="StopMultipleJobs"),
## JobStatus's
    url(r"^JobStatus", "revo.views.getJobStatus", name="JobStatus"),
## StopStatus's
    url(r"^stopJob", "revo.views.stopJob", name="stopJob"),
## Json's
    url(r"^Json", "revo.views.Json", name="Json"),
## Json2's
    url(r"^Json2", "revo.views.Json2", name="Json2"),
#SetTopBox
    url(r"^Set_Top_Box", "revo.views.GetSerialNum", name="Set_Top_Box"),



## Appium's
    url(r"^Appium", "app.views.Appium", name="Appium"),
	
## Storm's
    url(r"^Storm", "app.views.Storm", name="Storm"),


## Reports
    url(r"^Reports", "reports.views.reports_home", name="Reports"),
## Report's
#    url(r"^ReportsLink", "app.views.reportslink", name="ReportsLink"),

##Admin
    url(r"^admin/", include(admin.site.urls)),

)