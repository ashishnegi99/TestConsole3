from django.db import models
from django.core.validators import validate_ipv46_address as ip_validator
from django.core.urlresolvers import reverse_lazy

class Config(models.Model):
    name = models.CharField(max_length=255, unique=True)
    loc_fix = models.CharField(max_length=255)
    test_runner_path = models.CharField(max_length=255)
    report_location = models.CharField(max_length=255)
    run_path = models.CharField(max_length=255)
    json_path = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse_lazy('config_list')

    def __unicode__(self):
        return self.name


class TestCase(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse_lazy('test_case_list')

    def __unicode__(self):
        return self.name


class TestSuite(models.Model):
    name = models.CharField(max_length=255)
    cases = models.ManyToManyField(TestCase, related_name="testsuites")


class device(models.Model):
    device_type_choices = ( ('VMS', "VMS"), ('IMG', "IMG"), ('IPC2', "IPC2"), ('MKB', "MKB"),)
    
    name = models.CharField(max_length=255, unique=True)
    terminal_id = models.CharField(max_length=255, blank=True)
    unit_address = models.CharField(max_length=255)
    device_type = models.CharField(
        max_length=255,
        choices=device_type_choices,
        default='VM',
    )
    ip = models.GenericIPAddressField(protocol='both', validators=[ip_validator], blank=True, null=True)
    client_ip = models.GenericIPAddressField(protocol='both', validators=[ip_validator], blank=True, null=True)
    router = models.CharField(max_length=255, blank=True)
    host = models.CharField(max_length=255)
    environment = models.ForeignKey(Config, related_name="devices", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('device_list')

    def __unicode__(self):
        return self.name
