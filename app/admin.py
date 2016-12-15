from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

from app.models import Appium, Storm, racktestresult

admin.site.register(Appium)
admin.site.register(Storm)


class ResultResource(resources.ModelResource):
    class Meta:
        model = racktestresult
        import_id_fields = ('idTestResult',)
        fields = ('idTestResult', 'Date', 'ProjectName', 'TestJobName', 'TestJobExecutionId', 'SuiteName', 'TestCaseID', 'Author', 'Tester', 'BoxType', 'BoxUnitAddress', 'BoxIP', 'TotalActions', 'TotalConditions', 'PassNumbers', 'FailNumbers', 'Result', 'ExecutionTime')
        export_order = ('idTestResult', 'Date', 'ProjectName', 'TestJobName', 'TestJobExecutionId', 'SuiteName', 'TestCaseID', 'Author', 'Tester', 'BoxType', 'BoxUnitAddress', 'BoxIP', 'TotalActions', 'TotalConditions', 'PassNumbers', 'FailNumbers', 'Result', 'ExecutionTime')


class racktestresultAdmin(ImportExportModelAdmin):
	pass
	resource_class = ResultResource
	list_filter = ['Date']
	list_display = ('idTestResult', 'Date', 'ProjectName', 'TestJobName', 'TestJobExecutionId', 'SuiteName', 'TestCaseID', 'Author', 'Tester', 'BoxType', 'BoxUnitAddress', 'BoxIP', 'TotalActions', 'TotalConditions', 'PassNumbers', 'FailNumbers', 'Result', 'ExecutionTime')

admin.site.register(racktestresult, racktestresultAdmin)
