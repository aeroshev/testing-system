from django.urls import path

from .views import create_project, get_projects, home_page

urlpatterns = [
    path('<uuid:project_id>/', get_projects, name='get_project'),
    path('create/', create_project, name='create_project'),
    path('home/', home_page, name='home_project')
]
