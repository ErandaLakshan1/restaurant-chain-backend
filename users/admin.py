from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Fields to be displayed in the user list view
    list_display = ('username', 'email', 'user_type', 'mobile_number', 'address', 'nic')

    # Fields to be displayed in the user detail view (edit form)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info',
         {'fields': ('first_name', 'last_name', 'email', 'user_type', 'mobile_number', 'address', 'nic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to be displayed when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type', 'mobile_number', 'address', 'nic')}
         ),
    )



admin.site.register(CustomUser, CustomUserAdmin)
