from django.urls import path

from .views import (
    create_test_suite,
    get_edit_suite_page,
    get_report_page,
    get_test_case_page,
    get_test_plan_page,
    get_test_suite_page,
    get_edit_case_page,
    get_create_test_plan
)

urlpatterns = [
    path('plan/project/<uuid:project_id>/', get_test_plan_page, name='test_plan'),
    path('report/project/<uuid:project_id>/', get_report_page, name='test_report'),
    path('suites/project/<uuid:project_id>/', get_test_suite_page, name='test_suites'),
    path('suites/create/project/<uuid:project_id>/', create_test_suite, name='create_suite'),
    path('cases/project/<uuid:project_id>/', get_test_case_page, name='test_cases'),
    path('cases/edit/<uuid:testcase_id>/', get_edit_case_page, name='edit_case'),
    path('suites/edit/<uuid:suite_id>/', get_edit_suite_page, name='edit_suite'),
    path('plan/create/project/<uuid:project_id>/', get_create_test_plan, name='create_test_plan')

]
