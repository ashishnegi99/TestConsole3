from datetime import datetime
from django.conf.urls import patterns, include, url
from app.forms import BootstrapAuthenticationForm

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    

##Home
    url(r"^home", "app.views.home", name="home"),


##Home
    url(r"^$", "app.views.home", name="home"),

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

## Revo's

    url(r"^Revo", "app.views.Revo_view", name="Revo"),
	
## StopMultipleJobs's

    url(r"^StopMultipleJobs", "app.views.StopMultipleJobs", name="StopMultipleJobs"),

#SetTopBox
    url(r"^Set_Top_Box", "app.views.GetSerialNum", name="Set_Top_Box"),

## Storm's

    url(r"^Storm", "app.views.Storm", name="Storm"),

## Json's

    url(r"^Json", "app.views.Json", name="Json"),

## Json2's

    url(r"^Json2", "app.views.Json2", name="Json2"),


## JobStatus's

    url(r"^JobStatus", "app.views.getJobStatus", name="JobStatus"),

## StopStatus's

    url(r"^stopJob", "app.views.stopJob", name="stopJob"),

## Date Picker's

    # url(r"^Datepicker", "app.views.search", name="Datepicker"),

## Appium's
    url(r"^Appium", "app.views.Appium", name="Appium"),

## Report's
    url(r"^Reports", "reports.views.reports_home", name="Reports"),

## Report's
    url(r"^ReportsLink", "app.views.reportslink", name="ReportsLink"),

##Admin
    url(r"^admin/", include(admin.site.urls)),

)
