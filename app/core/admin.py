from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
# this is a recommanded conversion to convert strings to human readable.
# extend the code to support multiple languages
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']

    # fields to be included in list users page
    list_display = ['email', 'name']

    # fields to be included on change user page (edit page)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
         ),
        (_('Important dates'), {'fields': ('last_login',)})
    )

    # fields to be included in add user page
    # therefore we can create a new user with email and password
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


# If we use the default admin class, we dont have to pass the second parameter
# Here we modified the default adin class
admin.site.register(models.User, UserAdmin)