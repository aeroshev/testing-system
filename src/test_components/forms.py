from django import forms

from .models import Report, TestRun


class TestSuiteForm(forms.Form):
    ...


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
