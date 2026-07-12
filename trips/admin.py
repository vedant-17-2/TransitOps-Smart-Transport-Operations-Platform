from django.contrib import admin
from .models import Trip

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'driver', 'source', 'destination', 'status', 'start_date')
    list_filter = ('status',)
    search_fields = ('source', 'destination', 'vehicle__registration_number', 'driver__name')
