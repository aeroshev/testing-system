from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from project.models import Project
from project.forms import ProjectForm


class IndexView(TemplateView):
    """Тест"""
    template_name = 'index.html'


@require_GET
def get_projects(request: HttpRequest, project_id: UUID) -> HttpResponse:
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_page.html', project)


@require_POST
def create_project(request: HttpRequest) -> HttpResponse:
    form = ProjectForm(request.user, request.POST, request.FILES)
    if form.is_valid():
        return HttpResponse(status=202)
    return HttpResponse(status=404)
