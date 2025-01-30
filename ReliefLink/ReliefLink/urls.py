# ReliefLink/urls.py
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('home.urls')),
    path('account/', include('account.urls')),
    path('status/', include('Status.urls')),
]