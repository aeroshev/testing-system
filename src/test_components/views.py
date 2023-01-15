from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from project.models import Project
from .forms import TestSuiteForm, UploadReportForm
from .models import Report, TestCase, TestRun, TestSuite
from testflow.context import selected_project_id


@require_GET
@login_required
def get_test_plan_page(request: HttpRequest) -> HttpResponse:
    """Получить страницу тест плана проекта"""
    project_id = selected_project_id.get()
    runs = TestRun.objects \
        .filter(project__id=project_id) \
        .values("id", "status", "name", "running_by__username") \
        .annotate(tester=F('running_by__username'))[:5]

    return render(request, 'testing_page.html', {"suites": runs, "project_id": project_id})


@require_GET
@login_required
def get_test_suite_page(request: HttpRequest) -> HttpResponse:
    """Получить страницу создания тестового набора"""
    project_id = selected_project_id.get()
    context = {
        "suites": TestSuite.objects.filter(project__id=project_id),
        "create_form": TestSuiteForm(project_id),
        "project": Project.objects.get(id=project_id)
    }
    return render(request, 'suites_page.html', context)


@require_GET
@login_required
def get_test_case_page(request: HttpRequest) -> HttpResponse:
    """Получить страницу редактирования тест кейсов"""
    context = {
        "testcases": TestCase.objects.all()[:5],
        "project": Project.objects.get(id=selected_project_id.get())
    }
    return render(request, 'edit_testcase.html', context)


@require_GET
@login_required
def get_report_page(request: HttpRequest) -> HttpResponse:
    """Получить страницу загрузки отчёта о тестировании"""
    context = {
        'project': Project.objects.values("name", "description", "id").get(id=selected_project_id.get()),
        'report_form': UploadReportForm()
    }
    return render(request, 'create_report.html', context)


@require_GET
@login_required
def get_edit_suite_page(request: HttpRequest, suite_id: UUID) -> HttpResponse:
    """Получить страницу редактирования тестового набора"""
    return render(request, 'edit_suite.html')


@require_POST
@login_required
def create_test_suite(request: HttpRequest) -> HttpResponse:
    """Создать тестовый набор"""
    project_id = selected_project_id.get()
    form = TestSuiteForm(project_id, request.POST)
    if form.is_valid():
        suite = form.save()
        return redirect(reverse('edit_suite', args=(suite.id,)))
    else:
        context = {
            "suites": TestSuite.objects.filter(project__id=project_id),
            "create_form": TestSuiteForm(project_id),
            "project": Project.objects.get(id=project_id)
        }
        return render(request, 'suites_page.html', context)


@require_GET
@login_required
def get_edit_case_page(request: HttpRequest, testcase_id: UUID) -> HttpResponse:
    """Получить страницу редактирования тесткейса"""
    return render(request, 'edit_testcase.html')


@require_POST
@login_required
def load_report(request: HttpRequest) -> HttpResponse:
    form = UploadReportForm(request.POST, request.FILES)
    project = Project.objects.get(id=selected_project_id.get())
    if form.is_valid():
        report = project.test_runs.reports
        form.save(report)
    context = {
        'project': project,
        'report_form': UploadReportForm()
    }
    return render(request, 'create_report.html', context)
