from django.urls import path

from .views import (
    create_test_suite,
    get_edit_suite_page,
    get_report_page,
    get_test_case_page,
    get_test_plan_page,
    get_test_suite_page,
    get_edit_case_page,
    load_report
)

urlpatterns = [
    path('plan/', get_test_plan_page, name='test_plan'),
    path('report/', get_report_page, name='test_report'),
    path('report/upload/', load_report, name='test_load_report'),
    path('suites/', get_test_suite_page, name='test_suites'),
    path('suites/create/', create_test_suite, name='create_suite'),
    path('suites/edit/<uuid:suite_id>/', get_edit_suite_page, name='edit_suite'),
    path('cases/project/', get_test_case_page, name='test_cases'),
    path('cases/edit/<uuid:testcase_id>/', get_edit_case_page, name='edit_case')
]
