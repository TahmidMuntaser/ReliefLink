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
from .models import Division, District, Upazila, Union, Ward, Housh

from .models import DivisionalCommissionar, DeputyCommissionar, UNO, UnionChairman, WardMember

class DivisionalCommissionarAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'division']
    exclude = ['password']

class DeputyCommissionarAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'district']
    exclude = ['password']

class UNOAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'upazila']
    exclude = ['password']

class UnionChairmanAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'union']
    exclude = ['password']

class WardMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'ward']
    exclude = ['password']


admin.site.register(Division)
admin.site.register(District)
admin.site.register(Upazila)
admin.site.register(Union)
admin.site.register(Ward)
admin.site.register(Housh)


admin.site.register(DivisionalCommissionar, DivisionalCommissionarAdmin)
admin.site.register(DeputyCommissionar, DeputyCommissionarAdmin)
admin.site.register(UNO, UNOAdmin)
admin.site.register(UnionChairman, UnionChairmanAdmin)
admin.site.register(WardMember, WardMemberAdmin)