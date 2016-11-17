from django.db import models

class testsuite(models.Model):
    name = models.CharField(max_length=255)