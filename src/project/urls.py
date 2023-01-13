from django.urls import path

from project.views import get_projects, create_project, home_page, find_project

urlpatterns = [
    path('<uuid:project_id>/', get_projects, name='get_project'),
    path('create/', create_project, name='create_project'),
    path('home/', home_page, name='home_project'),
    path('find/', find_project, name='find_project')
]
