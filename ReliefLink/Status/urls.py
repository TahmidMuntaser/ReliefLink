# Status/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.status, name="status"),

    path('District Status/<int:division_id>/', views.district_status, name="district_status"),

    path('Upazila Status/<int:district_id>/', views.upazila_status, name="upazila_status"),

    path('Union Status/<int:upazila_id>/', views.union_status, name="union_status"),

    path('Ward Status/<int:union_id>/', views.ward_status, name="ward_status"),
]