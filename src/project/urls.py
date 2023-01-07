from django.urls import path

from project.views import IndexView, get_projects, create_project

urlpatterns = [
    path('', IndexView.as_view()),
    path('<uuid:project_id>/', get_projects),
    path('create/', create_project)
]
