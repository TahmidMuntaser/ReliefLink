from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('signup_success/', views.signup_success, name='signup_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dc_dashboard/', views.dc_dashboard, name='dc_dashboard'),
    path('uno_dashboard/', views.uno_dashboard, name='uno_dashboard'),
    path('public_dashboard/', views.public_dashboard, name='public_dashboard'),
]