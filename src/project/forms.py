from django import forms

from .models import Project, User
from test_components.models import TestRun, Report


class ProjectForm(forms.Form):
    """Форма для создания проекта"""
    name = forms.CharField(
        max_length=512,
        widget=forms.TextInput(attrs={'placeholder': 'Название проекта'}),
        required=True
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Описание проекта'})
    )

    def __init__(self, user: User, *args, **kwargs) -> None:
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self) -> Project:
        data = self.cleaned_data
        name = data['name']
        description = data['description']
        status = 'Created'
        manager = self.user

        project = Project.objects.create(
            name=name,
            description=description,
            status=status,
            manager=manager
        )
        test_run = TestRun.objects.create(
            name=f"Тестовый план проекта {project.name}"
        )
        Report.objects.create(
            name=f"Отчёт о тестировании проекта {project.name}",
            description=project.description,
            test_run=test_run
        )

        return project
