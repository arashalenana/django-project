from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'phone_number', 'address']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'address']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'address')}),
    )
admin.site.register(User, CustomUserAdmin)