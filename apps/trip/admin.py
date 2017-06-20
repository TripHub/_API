from django.contrib import admin

from .models import Trip


class TripAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'uid', 'created',)
    filter_horizontal = ('members',)

admin.site.register(Trip, TripAdmin)
