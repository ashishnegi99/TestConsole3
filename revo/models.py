from django.db import models

class testsuite(models.Model):
    name = models.CharField(max_length=255)
    mapping_name = models.CharField(max_length=255)

class device(models.Model):
	device_type_choices = ( ('VM', "VM"), ('IPC', "IPC"), ('MKB', "MKB"),)
	name = models.CharField(max_length=255, blank=False)
	mac_id = models.CharField(max_length=255, unique=True, blank=False)
	serial_id = models.CharField(max_length=255)
	device_type = models.CharField(
    	max_length=255,
    	choices=device_type_choices,
    	default='VM',
	)
	ip = models.GenericIPAddressField(protocol='IPv4')
	router = models.CharField(max_length=255)