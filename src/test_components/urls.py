from django.urls import path

from .views import get_test_plan_page, get_report_page, get_test_case_page

urlpatterns = [
    path('plan/project/<uuid:project_id>/', get_test_plan_page, name='test_plan'),
    path('report/project/<uuid:project_id>/', get_report_page, name='test_report'),
    path('cases/', get_test_case_page, name='test_cases')
]
