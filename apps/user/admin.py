from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)

admin.site.register(User, UserAdmin)
