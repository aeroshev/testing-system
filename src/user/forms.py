from django import forms

from .models import User, UserRole


class SignupForm(forms.Form):
    """Форма создания пользователя"""
    username = forms.CharField(
        max_length=512,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        required=True
    )
    role = forms.ChoiceField(
        choices=UserRole.choices,
        required=True
    )
    password = forms.CharField(
        max_length=512,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=True
    )
    confirm_password = forms.CharField(
        max_length=512,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        required=True
    )

    def clean(self) -> None:
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError('password and confirm_password does not match')

    def save(self) -> User:
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        role = self.cleaned_data['role']

        return User.objects.create_user(
            username=username,
            password=password,
            role=role
        )

    class Meta:
        model = User
        fields = ('username', 'password')


class LoginForm(forms.Form):
    """Форма аутентификации пользователя"""
    username = forms.CharField(
        max_length=512,
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        required=True
    )
    password = forms.CharField(
        max_length=512,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=True
    )
