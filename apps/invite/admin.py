from django.contrib import admin

from .models import Invite


class InviteAdmin(admin.ModelAdmin):
    list_display = ('uid', 'trip', 'email', 'status',)


admin.site.register(Invite, InviteAdmin)
