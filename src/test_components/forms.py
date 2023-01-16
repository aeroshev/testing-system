from uuid import UUID

from django import forms

from project.models import Project
from .models import Report, TestRun, TestSuite, TestCase


class ReportForm(forms.Form):
    """Форма для создания отчёта"""
    name = forms.CharField(max_length=512)
    description = forms.CharField()
    test_run_id = forms.UUIDField()

    def save(self) -> Report:
        data = self.cleaned_data
        name = data['name']
        description = data['description']
        test_run_id = data['test_run_id']

        test_run = TestRun.objects.get(id=test_run_id)
        return Report.objects.create(
            name=name,
            description=description,
            test_run=test_run
        )


class UploadReportForm(forms.Form):
    """Для загрузки отчёта"""
    file = forms.FileField()

    def save(self, report: Report) -> Report:
        report.update(file=self.cleaned_data['file'])
        return report


class TestSuiteForm(forms.Form):
    """Форма для создания тестового набора"""
    name = forms.CharField(
        max_length=512,
        widget=forms.TextInput(attrs={'placeholder': 'Название набора...'})
    )

    def __init__(self, project_id: UUID, *args, **kwargs) -> None:
        super(TestSuiteForm, self).__init__(*args, **kwargs)
        self.project_id = project_id

    def save(self) -> TestSuite:
        project = Project.objects.get(id=self.project_id)

        return TestSuite.objects.create(
            name=self.cleaned_data['name'],
            project=project
        )

class TestCaseForm(forms.Form):
    """Форма для создания тестового набора"""
    name = forms.CharField(
        max_length=512,
        widget=forms.TextInput(attrs={'placeholder': 'Название тест-кейса...'})
    )

    def __init__(self, project_id: UUID, *args, **kwargs) -> None:
        super(TestCaseForm, self).__init__(*args, **kwargs)

    def save(self) -> TestCase:
        return TestCase.objects.create(
            name=self.cleaned_data['name'],
            executed_code=0
        )


class EditTestCaseForm(forms.Form):
    """Форма для создания тестового набора"""

    steps = forms.CharField(
        max_length=512,
        widget=forms.TextInput(attrs={'placeholder': 'Шаги тест-кейса...'})
    )


    conds = forms.CharField(
        max_length=512,
        widget=forms.TextInput(attrs={'placeholder': 'Условия тест-кейса...'})
    )

    def __init__(self, case_id: UUID, *args, **kwargs) -> None:
        super(EditTestCaseForm, self).__init__(*args, **kwargs)
        self.case_id = case_id

    def update(self) -> TestCase:
        case = TestCase.objects.get(id=self.case_id)
        case.steps =self.cleaned_data['steps'],
        case.conditions = self.cleaned_data['conds'],
        case.save()
        return case

