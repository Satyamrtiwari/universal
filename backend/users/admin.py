from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'phone_number', 'role', 'area_village', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'age', 'phone_number', 'address', 'area_village', 'pincode')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'age', 'phone_number', 'address', 'area_village', 'pincode')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
