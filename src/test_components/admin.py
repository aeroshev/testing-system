from django.contrib import admin

from .models import Report, TestCase, TestRun, TestSuite

admin.site.register(TestSuite)
admin.site.register(TestRun)
admin.site.register(TestCase)
admin.site.register(Report)
