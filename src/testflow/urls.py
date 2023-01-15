from django.contrib import admin
from django.urls import include, path

from user.views import login_page, redirect_to_start

urlpatterns = [
    path('admin/', admin.site.urls),
    path('project/', include('project.urls')),
    path('user/', include('user.urls')),
    path('tests/', include('test_components.urls')),
    path('', redirect_to_start, name='index'),
    path('start/', login_page, name='start')
]
