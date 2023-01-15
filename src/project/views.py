from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .forms import ProjectForm
from .models import Project


<<<<<<< HEAD
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

=======
@require_GET
@login_required
def get_projects(request: HttpRequest, project_id: UUID) -> HttpResponse:
    """Получить страницу проекта"""
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_page.html', {'project': project})


@require_GET
@login_required
def home_page(request: HttpRequest) -> HttpResponse:
    """Получить домашнюю страницу системы"""
    context = {
        'projects': Project.objects.all().values("id", "name", "status"),
        'create_form': ProjectForm(request.user)
    }
    return render(request, 'index.html', context)


@require_POST
@login_required
def create_project(request: HttpRequest) -> HttpResponse:
    """Форма создания нового проекта"""
    form = ProjectForm(request.user, request.POST)
    if form.is_valid():
        project = form.save()
        return redirect(reverse('get_project', args=(project.id,)))
    return HttpResponse(status=404)
>>>>>>> develop_eroshev
