from django.urls import path

from user.views import login_user, signup_user

urlpatterns = [
    path('login/', login_user),
    path('signup/', signup_user),
]
