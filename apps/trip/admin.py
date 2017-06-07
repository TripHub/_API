from django.contrib import admin

from .models import Trip


class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'uid', 'created',)

admin.site.register(Trip, TripAdmin)
