from django.urls import path

from user.views import login_user, signup_user, logout_user

urlpatterns = [
    path('login/', login_user, name="login_user"),
    path('signup/', signup_user, name="signup_user"),
    path("logout/", logout_user, name="logout_user")
]
