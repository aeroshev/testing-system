from django.urls import path

<<<<<<< HEAD
from project.views import IndexView
from project.views import CreateReportView
from project.views import CreateSuiteView
from project.views import ProjectPageView
from project.views import EditCaseView
from project.views import PerformSuiteView
from project.views import TestingPageView

urlpatterns = [
    path('', IndexView.as_view()),
    path('create_report/', CreateReportView.as_view()),
    path('create_suite/',  CreateSuiteView.as_view()),
    path('project_page/',  ProjectPageView.as_view()),
    path('edit_testcase/',  EditCaseView.as_view()),
    path('perform_suite/',  PerformSuiteView.as_view()),
    path('testing_page/',  TestingPageView.as_view())
=======
from .views import create_project, get_projects, home_page

urlpatterns = [
    path('<uuid:project_id>/', get_projects, name='get_project'),
    path('create/', create_project, name='create_project'),
    path('home/', home_page, name='home_project')
>>>>>>> develop_eroshev
]
