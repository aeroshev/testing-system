from django.urls import path

from project.views import IndexView

urlpatterns = [
    path('', IndexView.as_view())
]
