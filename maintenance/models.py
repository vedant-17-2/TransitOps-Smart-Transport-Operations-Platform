from django.db import models
from core.models import BaseModel

class MaintenanceRecord(BaseModel):
    class MaintenanceType(models.TextChoices):
        OIL_CHANGE = 'oil_change', 'Oil Change'
        TYRE = 'tyre', 'Tyre Replacement'
        ENGINE = 'engine', 'Engine Repair'
        BRAKE = 'brake', 'Brake Service'
        GENERAL = 'general', 'General Service'

    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        COMPLETED = 'completed', 'Completed'

    vehicle = models.ForeignKey('fleet.Vehicle', on_delete=models.CASCADE, related_name='maintenance_records')
    maintenance_type = models.CharField(max_length=20, choices=MaintenanceType.choices)
    description = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    completed_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_maintenance_type_display()} - {self.vehicle}"

    @property
    def status_css_class(self):
        return f"status-{self.status}"
