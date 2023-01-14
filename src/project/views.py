from uuid import UUID

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from project.models import Project
from project.forms import ProjectForm, FindProjectFrom


@require_GET
@login_required
def get_projects(request: HttpRequest, project_id: UUID) -> HttpResponse:
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_page.html', {'project': project})


@require_GET
@login_required
def home_page(request: HttpRequest) -> HttpResponse:
    context = {
        'projects': Project.objects.all().values("id", "name")[:5],
        'create_form': ProjectForm(request.user)
    }
    return render(request, 'index.html', context)


@require_POST
@login_required
def create_project(request: HttpRequest) -> HttpResponse:
    form = ProjectForm(request.user, request.POST)
    if form.is_valid():
        project = form.save()
        return redirect(reverse('get_project', args=(project.id,)))
    return HttpResponse(status=404)


@require_POST
@login_required
def find_project(request: HttpRequest) -> HttpResponse:
    form = FindProjectFrom(request.POST)
    if form.is_valid():
        ...
