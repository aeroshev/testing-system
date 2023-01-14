from django.contrib import admin
from .models import TestSuite, TestRun, TestCase, Report


admin.site.register(TestSuite)
admin.site.register(TestRun)
admin.site.register(TestCase)
admin.site.register(Report)
