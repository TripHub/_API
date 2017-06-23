from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'auth0_id', 'uid', 'email', 'is_staff', 'is_active', 'created',)
    list_filter = ('is_staff', 'is_active',)

admin.site.register(User, UserAdmin)
