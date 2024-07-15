from django.contrib import admin
from .models import Account, Patient, Doctor
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    list_filter = ('is_active', 'is_superuser', 'is_doctor')
    ordering = ('email', 'username',)
    list_display = ('email', 'gender', 'username', 'first_name', 'last_name', 'phone_number', 'is_active', 'is_doctor')
    fieldsets = (
        ('User Profile', {'fields': ('image', 'gender', 'first_name', 'last_name')}),
        ('User Authentications', {'fields': ('email', 'username', 'phone_number')}),
        ('Wallet', {'fields': ('balance',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_doctor')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'gender', 'first_name', 'last_name',
                       'is_active', 'phone_number', 'is_doctor', 'balance')
        }

        ),
    )


admin.site.register(Account, UserAdminConfig)
admin.site.register(Patient)
admin.site.register(Doctor)
