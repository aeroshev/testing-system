from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from project.models import Project
from .forms import TestSuiteForm, TestCaseForm, EditTestCaseForm
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

    return render(request, 'testing_page.html', {"suites": runs, "project_id":project_id})


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
    project_id = selected_project_id.get()
    context = {
        "cases": TestCase.objects.all(),
        "create_form": TestCaseForm(project_id),
        "project": Project.objects.get(id=project_id)
    }
    return render(request, 'cases_page.html', context)



@require_GET
@login_required
def get_report_page(request: HttpRequest) -> HttpResponse:
    """Получить страницу загрузки отчёта о тестировании"""
    project_id = selected_project_id.get()
    context = {
        'project': Project.objects.get(id=project_id),
        'report': get_object_or_404(Report, test_run__project__id=project_id)
    }
    return render(request, 'create_report.html', context)


@require_GET
@login_required
def get_edit_suite_page(request: HttpRequest,  suite_id: UUID) -> HttpResponse:
    """Получить страницу редактирования тестового набора"""
    suit = TestSuite.objects.get(id = suite_id)
    cases = TestCase.objects.all()
    return render(request, 'edit_suite.html', context = {'cases':cases,  'testsuite': suit})

@require_GET
@login_required
def get_edit_case_page(request: HttpRequest,  case_id: UUID) -> HttpResponse:
    """Получить страницу редактирования тестового набора"""
    case = TestCase.objects.get(id = case_id)
    context = {
        'testcase': case,
        'cur_steps': ', '.join(case.steps),
        'cur_conds': ', '.join(case.conditions),
        "create_form": EditTestCaseForm(case_id)
    }
    return render(request, 'edit_case.html', context)


@require_POST
@login_required
def create_test_suite(request: HttpRequest) -> HttpResponse:
    project_id = selected_project_id.get()
    """Создать тестовый набор"""
    form = TestSuiteForm(project_id, request.POST)
    if form.is_valid():
        suite = form.save()
        return redirect(reverse('edit_suite', args=(suite.id,)))
    return HttpResponse(status=404)

@require_POST
@login_required
def create_test_case(request: HttpRequest) -> HttpResponse:
    """Создать тестовый набор"""
    project_id = selected_project_id.get()
    form = TestCaseForm(project_id, request.POST)
    if form.is_valid():
        case = form.save()
        return redirect(reverse('edit_case', args=(case.id,)))
    return HttpResponse(status=404)

@require_POST
@login_required
def update_test_case(request: HttpRequest, case_id: UUID) -> HttpResponse:
    """Создать тестовый набор"""
    form = EditTestCaseForm(case_id, request.POST)
    if form.is_valid():
        case = form.update()
        return redirect(reverse('edit_case', args=(case.id,)))
    return HttpResponse(status=404)


@require_GET
@login_required
def get_create_test_plan(request: HttpRequest) -> HttpResponse:
    """Получить страницу редактирования тесткейса"""
    project_id = selected_project_id.get()
    suites = TestSuite.objects.all()
    context = {'project_id': project_id, 'testsuites': suites}
    return render(request, 'create_testplan.html', context)