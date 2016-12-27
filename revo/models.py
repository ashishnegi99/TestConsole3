from django.db import models
from django.core.validators import validate_ipv46_address as ip_validator
from django.core.urlresolvers import reverse_lazy

class TestCase(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse_lazy('test_case_list')

    def __unicode__(self):
        return self.name


class TestSuite(models.Model):
    name = models.CharField(max_length=255)
    cases = models.ManyToManyField(TestCase, related_name="testcases")


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
    environment = models.CharField(max_length=255, default="SIT")