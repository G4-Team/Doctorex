from django.contrib import admin
from .models import Account, Patient, Doctor
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    ordering = ('email',)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff',)
        }

        ),
    )


admin.site.register(Account, UserAdminConfig)
admin.site.register(Patient)
admin.site.register(Doctor)
