from django.db import models
from django.core.validators import validate_ipv46_address as ip_validator


class testsuite(models.Model):
    name = models.CharField(max_length=255)
    mapping_name = models.CharField(max_length=255)

class device(models.Model):
	device_type_choices = ( ('VM', "VM"), ('IPC', "IPC"), ('MKB', "MKB"),)
	name = models.CharField(max_length=255, unique=True)
	mac_id = models.CharField(max_length=255, blank=True)
	serial_id = models.CharField(max_length=255)
	device_type = models.CharField(
    	max_length=255,
    	choices=device_type_choices,
    	default='VM',
	)
	ip = models.GenericIPAddressField(protocol='both', validators=[ip_validator], blank=True, null=True)
	router = models.CharField(max_length=255)
	host = models.CharField(max_length=255, blank=True)