from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required


@require_GET
@login_required
def get_test_plan_page(request: HttpRequest) -> HttpResponse:
    return render()
