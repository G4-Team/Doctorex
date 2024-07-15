from django.contrib import admin
from .models import Account, Patient, Doctor, VisitTime
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    list_filter = ('is_active', 'is_staff', 'is_superuser',)
    ordering = ('email',)
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'username')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'image',
                       'is_active', 'is_staff',)
        }

        ),
    )


class VisitTimeAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'weekday', 'start_time', 'end_time', 'is_reserved')
    list_filter = ('doctor', 'weekday', 'is_reserved')
    search_fields = ('doctor__account', 'weekday')
    list_editable = ('is_reserved',)


admin.site.register(Account, UserAdminConfig)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(VisitTime, VisitTimeAdmin)
