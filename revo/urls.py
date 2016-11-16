from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='revo'),
    
    url(r'^revo_view/$', views.revo_view, name='revo_view'),
	
    url(r'^console/$', views.consolelink, name='consolelink'),
	## StopMultipleJobs's
    url(r"^StopMultipleJobs", views.StopMultipleJobs, name="StopMultipleJobs"),
## JobStatus's
    url(r"^JobStatus", views.getJobStatus, name="JobStatus"),
## StopStatus's
    url(r"^stopJob", views.stopJob, name="stopJob"),
## Json's
    url(r"^Json", views.Json, name="Json"),
## Json2's
    url(r"^Json2", views.Json2, name="Json2"),
#SetTopBox
    url(r"^Set_Top_Box", views.GetSerialNum, name="Set_Top_Box"),
#Console output
    # url(r"^ConsoleLink", "revo.views.consolelink", name="ConsoleLink"),

]