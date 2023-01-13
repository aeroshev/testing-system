from django import forms

from .models import Project, User


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

        return Project.objects.create(
            name=name,
            description=description,
            status=status,
            manager=manager
        )


class FindProjectFrom(forms.Form):
    """Форма для поиска проекта"""
    name = forms.CharField(
        max_length=512,
        widget=forms.TextInput(attrs={'placeholder': 'Поиск...'}),
        required=True
    )
