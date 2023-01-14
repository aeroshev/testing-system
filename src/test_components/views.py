from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .models import TestRun, Report, TestCase
from project.models import Project


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
def get_test_suite_page(request: HttpRequest) -> HttpResponse:
    """Получить страницу создания тестового набора"""
    ...


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

