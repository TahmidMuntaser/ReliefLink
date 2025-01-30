# Status/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.status, name="status"),
    path('District Status/<int:division_id>/', views.district_status, name="district_status"),
]