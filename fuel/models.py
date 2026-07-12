from django.db import models
from core.models import BaseModel

class FuelLog(BaseModel):
    trip = models.ForeignKey('trips.Trip', on_delete=models.CASCADE, null=True, blank=True, related_name='fuel_logs')
    vehicle = models.ForeignKey('fleet.Vehicle', on_delete=models.CASCADE, related_name='fuel_logs')
    fuel_quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text='Liters')
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Fuel: {self.fuel_quantity}L - {self.vehicle}"

class Expense(BaseModel):
    class ExpenseType(models.TextChoices):
        FUEL = 'fuel', 'Fuel'
        MAINTENANCE = 'maintenance', 'Maintenance'
        TOLL = 'toll', 'Toll'
        DRIVER_SALARY = 'driver_salary', 'Driver Salary'
        INSURANCE = 'insurance', 'Insurance'
        OTHER = 'other', 'Other'

    vehicle = models.ForeignKey('fleet.Vehicle', on_delete=models.CASCADE, related_name='expenses')
    expense_type = models.CharField(max_length=20, choices=ExpenseType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_expense_type_display()}: {self.amount}"
