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

##Test Console main app
    url(r"^home", "app.views.home", name="home"),
    url(r"^$", "app.views.home", name="home"),

## Revo's
    url(r'^revo/', include('revo.urls')),

## Appium's
    url(r"^Appium", "app.views.Appium", name="Appium"),
	
## Storm's
    url(r"^Storm", "app.views.Storm", name="Storm"),

## Reports
    url(r"^Reports", "reports.views.reports_home", name="Reports"),

##Admin
    url(r"^admin/", include(admin.site.urls)),

)