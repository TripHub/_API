from django.contrib import admin

from .models import Invite


class InviteAdmin(admin.ModelAdmin):
    list_display = ('uid', 'trip', 'email',)


admin.site.register(Invite, InviteAdmin)
