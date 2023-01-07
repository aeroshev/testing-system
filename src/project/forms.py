from django import forms

from .models import Project, User


class ProjectForm(forms.Form):
    """Форма для создания проекта"""
    name = forms.CharField(max_length=512)

    def __init__(self, user: User, *args, **kwargs) -> None:
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.user = user

    def save(self) -> Project:
        data = self.cleaned_data
        name = data['name']
        status = 'Created'
        manager = self.user

        return Project.objects.create(
            name=name,
            status=status,
            manager=manager
        )


class TestSuiteForm(forms.Form):
    ...
