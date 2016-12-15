from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='revo'),
    
    url(r'^revo_view/$', views.revo_view, name='revo_view'),
# Console output	
    url(r'^console/$', views.consolelink, name='consolelink'),
# StopMultipleJobs's
    url(r"^StopMultipleJobs", views.StopMultipleJobs, name="StopMultipleJobs"),
# JobStatus's
    url(r"^JobStatus", views.getJobStatus, name="JobStatus"),
# StopStatus's
    url(r"^stopJob", views.stopJob, name="stopJob"),
# Json's
    url(r"^Json", views.Json, name="Json"),
# Json2's
    url(r"^Json2", views.Json2, name="Json2"),
# SetTopBox
    url(r"^Set_Top_Box", views.GetSerialNum, name="Set_Top_Box"),
# testsuite
    url(r"^test_suites/list_view", views.test_suites_list, name="test_suite_list"),
    url(r"^test_suite/add_view", views.test_suites_add_view, name="test_suites_add_view"),
    url(r"^testsuite/new", views.add_test_suite, name="test_suite_new"),
    url(r"^testsuite/delete", views.delete_test_suite, name="test_suite_delete"),
# device
    url(r"^devices/list_view", views.device_list, name="device_list"),
    url(r"^device/add_view", views.device_add_view, name="device_add_view"),
    url(r"^device/new", views.add_device, name="device_new"),
    url(r"^device/delete", views.delete_device, name="device_delete"),
    url(r"^device/", views.device, name="device"),
# configs
    url(r"^configs/", views.configs, name="configs_view"),
    url(r"^configs_add", views.add_configurations, name="configs_add"),
]