from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .forms import LoginForm, SignupForm


@require_GET
def login_page(request: HttpRequest) -> HttpResponse:
    """
    Если пользователь уже авторизован в системе, то направить на домашнюю страницу
    Если пользователь новый, то направить на стартовую страницу
    """
    if request.user.is_authenticated:
        return redirect('/project/home')
    else:
        context = {
            'signup': SignupForm(),
            'login': LoginForm()
        }
        return render(request, 'authentication.html', context)


@require_GET
def redirect_to_start(request: HttpRequest) -> HttpResponse:
    """Перенаправить на стартовую страницу"""
    return redirect('/start')


@require_POST
def login_user(request: HttpRequest) -> HttpResponse:
    """Авторизовать пользователя"""
    form = LoginForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        user = authenticate(
            request,
            username=cleaned_data['username'],
            password=cleaned_data['password']
        )
        if user is not None:
            login(request, user)

            return redirect('/project/home')

    return redirect('/start')


@require_POST
@login_required
def logout_user(request: HttpRequest) -> HttpResponse:
    """Выйти из системы"""
    return redirect('/start')


@require_POST
def signup_user(request: HttpRequest) -> HttpResponse:
    """Зарегистрировать нового пользователя"""
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('/project/home')
    else:
        return redirect('/start')
