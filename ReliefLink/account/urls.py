# account/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),

    path('password_update/', views.updatepassword_view, name='update_password'),

    path('add_user/', views.add_user_view, name='add_user'),

    path('add_divisionalcommissioner/', views.add_divisionalcommissioner_view, name='add_divisionalcommissioner'),

    path('add_deputycommissioner/', views.add_deputycommissioner_view, name='add_deputycommissioner'),

    path('add_uno/', views.add_uno_view, name='add_uno'),

    path('add_unionchairman/', views.add_unionchairman_view, name='add_unionchairman'),

    path('add_wardmember/', views.add_wardmember_view, name='add_wardmember'),

    path('add_house/', views.add_house_view, name='add_house'),


]