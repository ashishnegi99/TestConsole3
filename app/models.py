from django.db import models
from django.contrib.auth.models import User
import datetime

class Appium(models.Model):            
    name = models.CharField(max_length=30)
    details = models.TextField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Appium"


class Storm(models.Model):           
    name = models.CharField(max_length=30)
    details = models.TextField(blank = True)
    date = models.DateTimeField()
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Storm"


class racktestresult(models.Model):
    idTestResult = models.IntegerField()
    Date = models.DateField()
    ProjectName = models.CharField(max_length=255)
    TestJobName = models.CharField(max_length=255)
    TestJobExecutionId = models.CharField(max_length=255)
    SuiteName = models.CharField(max_length=255)
    TestCaseID = models.CharField(max_length=255)
    Author = models.CharField(max_length=255)
    Tester = models.CharField(max_length=255)
    BoxType = models.CharField(max_length=255)
    BoxUnitAddress = models.CharField(max_length=255)
    BoxIP = models.CharField(max_length=255)
    TotalActions = models.IntegerField()
    TotalConditions = models.IntegerField()
    PassNumbers = models.IntegerField()
    FailNumbers = models.IntegerField()
    Result = models.CharField(max_length=255)
    ExecutionTime = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Rack Test Result"