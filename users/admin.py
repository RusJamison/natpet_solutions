from django.contrib import admin
from .models import User, Profile
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address_line_1', 'address_line_2', 'city','phone_number']
    list_filter = ['user', 'country', 'city']
    search_fields = ['user__username', 'phone_number', 'city']
