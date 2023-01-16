from django.urls import path

from .views import (
    create_test_suite,
    get_edit_suite_page,
    get_report_page,
    get_test_case_page,
    get_test_plan_page,
    get_test_suite_page,
    create_test_case,
    get_create_test_plan,
    get_edit_case_page,
    update_test_case
)

urlpatterns = [
    path('plan/', get_test_plan_page, name='test_plan'),
    path('report/', get_report_page, name='test_report'),
    path('suites/', get_test_suite_page, name='test_suites'),
    path('cases/', get_test_case_page, name='test_cases'),

    path('suites/create/project/', create_test_suite, name='create_suite'),
    path('cases/create/', create_test_case, name='create_case'),

    path('suites/edit/<uuid:suite_id>/', get_edit_suite_page, name='edit_suite'),
    path('cases/edit/<uuid:case_id>/', get_edit_case_page, name='edit_case'),

    path('cases/update/<uuid:case_id>/', update_test_case, name='update_case'),

    path('plan/create/', get_create_test_plan, name='create_test_plan')

]
