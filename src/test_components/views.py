from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from project.models import Project
from .forms import TestSuiteForm
from .models import Report, TestCase, TestRun, TestSuite


@require_GET
@login_required
def get_test_plan_page(request: HttpRequest, project_id: UUID) -> HttpResponse:
    """Получить страницу тест плана проекта"""
    runs = TestRun.objects \
        .filter(project__id=project_id) \
        .values("id", "status", "name", "running_by__username") \
        .annotate(tester=F('running_by__username'))[:5]

    return render(request, 'testing_page.html', {"suites": runs})


@require_GET
@login_required
def get_test_suite_page(request: HttpRequest, project_id: UUID) -> HttpResponse:
    """Получить страницу создания тестового набора"""
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
    cases = TestCase.objects.all()[:5]
    return render(request, 'edit_testcase.html', {'test_cases': cases})


@require_GET
@login_required
def get_report_page(request: HttpRequest, project_id: UUID) -> HttpResponse:
    """Получить страницу загрузки отчёта о тестировании"""
    context = {
        'project': Project.objects.values("name", "description").get(id=project_id),
        'report': get_object_or_404(Report, test_run__project__id=project_id)
    }
    return render(request, 'create_report.html', context)


@require_GET
@login_required
def get_edit_suite_page(request: HttpRequest, suite_id: UUID) -> HttpResponse:
    """Получить страницу редактирования тестового набора"""
    return render(request, 'edit_suite.html')


@require_POST
@login_required
def create_test_suite(request: HttpRequest, project_id: UUID) -> HttpResponse:
    """Создать тестовый набор"""
    form = TestSuiteForm(project_id, request.POST)
    if form.is_valid():
        suite = form.save()
        return redirect(reverse('edit_suite', args=(suite.id,)))
    return HttpResponse(status=404)


