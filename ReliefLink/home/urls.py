from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),  # Keep this one
    path('service/', views.service, name='service'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),  # Add this line
    path('logout/', views.logout_view, name='logout'),  # Add this line
]