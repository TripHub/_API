from django.contrib import admin

from .models import Trip, Destination


class TripAdmin(admin.ModelAdmin):
    list_display = ('uid', 'title', 'owner', 'created',)


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('trip', 'name', 'latitude', 'longitude',)

admin.site.register(Trip, TripAdmin)
admin.site.register(Destination)
