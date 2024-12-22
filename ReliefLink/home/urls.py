from django.urls import path, include
from . import views
from django.contrib.auth.urls import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dc_dashboard/', views.dc_dashboard, name='dc_dashboard'),
    path('uno_dashboard/', views.uno_dashboard, name='uno_dashboard'),
    path('public_dashboard/', views.public_dashboard, name='public_dashboard'),

    path('divisional_commissionar/', views.divisional_commissionar, name='divisional_commissionar'),

    path("register/", views.register, name='register'),

    path("accounts/", include('django.contrib.auth.urls')),
]