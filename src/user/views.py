from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse

from .forms import SignupForm, LoginForm


@require_GET
def login_page(request: HttpRequest) -> HttpResponse:
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
    return redirect('/start')


@require_POST
def login_user(request: HttpRequest) -> HttpResponse:
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
def logout_user(request: HttpRequest) -> HttpResponse:
    ...


@require_POST
def signup_user(request: HttpRequest) -> HttpResponse:
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('/project/home')
    else:
        return redirect('/start')
