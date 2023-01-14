from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from .forms import ProjectForm
from .models import Project


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
