from django.db import models

class testsuite(models.Model):
    name = models.CharField(max_length=255)
    mapping_name = models.CharField(max_length=255)