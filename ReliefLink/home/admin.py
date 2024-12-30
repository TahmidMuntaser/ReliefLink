from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Division, District, Upazila, Union, Ward, Housh



admin.site.register(Division)
admin.site.register(District)
admin.site.register(Upazila)
admin.site.register(Union)
admin.site.register(Ward)
admin.site.register(Housh)

CustomUser = get_user_model()

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'name')
    ordering = ('email',)
    list_filter = ('user_type', 'is_active')  # Add filtering by user type and is_active

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type')}),
        ('Groups and Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'user_type', 'is_staff', 'is_active'),
        }),
    )

# Register other models as usual
# admin.site.register(CustomUser, CustomUserAdmin)
