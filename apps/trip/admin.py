from django.contrib import admin

from .models import Trip


class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner',)

admin.site.register(Trip, TripAdmin)
