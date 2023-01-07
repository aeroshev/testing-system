from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Тест"""
    def get(self, request):
        projects = ['System1', 'System2', 'System3', 'System3', 'System3', 'System3']
        return render(request, 'index.html', context = {'projects': projects})


class CreateReportView(TemplateView):
    def get(self, request):
        descr = 'description'
        return render(request, 'create_report.html' , context = {'descr': descr})


class CreateSuiteView(TemplateView):
    def get(self, request):
        avail_testcases = ['TestCase1', 'TestCase2', 'TestCase3']
        sel_testcases = ['TestCase1', 'TestCase2', 'TestCase3', 'TestCase4']
        con = {'proj_name':'Проект 1', 'avail_testcases': avail_testcases, 'sel_testcases': sel_testcases}
        return render(request, 'create_suite.html' , context = con)

class ProjectPageView(TemplateView):
    def get(self, request):
        descr = 'description'
        return render(request, 'project_page.html' , context = {'descr': descr})


class EditCaseView(TemplateView):
    def get(self, request):
        testcases = ['TestCase1', 'TestCase2', 'TestCase3', 'TestCase4']
        con = {'proj_name':'Проект 1', 'testcases': testcases}
        return render(request, 'edit_testcase.html' , context = con)

class PerformSuiteView(TemplateView):
    def get(self, request):
        testcases = ['TestCase1', 'TestCase2', 'TestCase3', 'TestCase4']
        con = {'proj_name':'Проект 1', 'testcases': testcases}
        return render(request, 'perform_suite.html' , context = con)

class TestingPageView(TemplateView):
    def get(self, request):
        row1 = {'id':10, 'status':'ok', 'name':'case1', 'tester':'Oleg'}
        row2 = {'id': 20, 'status': 'ok', 'name': 'case2', 'tester': 'Oleg'}
        rows = [row1, row2]
        return render(request, 'testing_page.html' , context = {'rows':rows})

