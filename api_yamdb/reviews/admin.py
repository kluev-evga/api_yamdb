from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UsersAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'role', 'first_name', 'last_name', 'email', 'bio'
    )
    list_filter = ('role',)
    save_on_top = True
    save_as = True
