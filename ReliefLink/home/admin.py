# home/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Unregister the original User admin
admin.site.unregister(User)

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_active=True)
    approve_users.short_description = "Approve selected users"

# Register the new User admin
admin.site.register(User, UserAdmin)

# Register your models
from .models import YourModel
admin.site.register(YourModel)