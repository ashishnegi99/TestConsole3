from django.conf.urls import url
from . import views

# Conversion before production
# TODO: url = in lowercase and '-' separated
# TODO: name = in lowercase '_' separated
# function name = depending upon wether it is class or function

urlpatterns = [
	url(r'^$', views.home, name='revo'),
    
    url(r'^revo_view/$', views.revo_view, name='revo_view'),
    url(r'^run', views.run_job, name='revo_run'),
    
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
    url(r"^devices", views.DeviceList.as_view(), name="device_list"),
    url(r"^device/new$", views.DeviceCreate.as_view(), name="device_new"),
    url(r"^device/delete", views.delete_device, name="device_delete"),
    url(r'^device/edit/(?P<pk>\d+)/$', views.DeviceUpdate.as_view(), name='device_edit'),

# configs
    url(r"^configs/", views.configs, name="configs_view"),
    url(r"^configs_add", views.add_configurations, name="configs_add"),

# TestCase
    url(r'^test-case/$', views.TestCaseList.as_view(), name='test_case_list'),
    url(r'^test-case/new$', views.TestCaseCreate.as_view(), name='test_case_new'),
    url(r'^test-case/edit/(?P<pk>\d+)/$', views.TestCaseUpdate.as_view(), name='test_case_edit'),
    url(r'^test-case/delete', views.delete_test_case, name='test_case_delete'),
]