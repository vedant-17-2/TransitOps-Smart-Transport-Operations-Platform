from django.contrib import admin
from .models import FuelLog, Expense

@admin.register(FuelLog)
class FuelLogAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'trip', 'fuel_quantity', 'cost', 'date')
    list_filter = ('date',)
    search_fields = ('vehicle__registration_number',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'expense_type', 'amount', 'date')
    list_filter = ('expense_type', 'date')
    search_fields = ('vehicle__registration_number', 'description')
