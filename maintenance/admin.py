from django.contrib import admin
from .models import MaintenanceRecord

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'maintenance_type', 'date', 'cost', 'status')
    list_filter = ('status', 'maintenance_type')
    search_fields = ('vehicle__registration_number', 'description')
