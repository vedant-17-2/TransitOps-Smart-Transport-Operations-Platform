from django.db import models
from django.contrib.auth.models import User
from core.models import BaseModel

class Trip(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        DISPATCHED = 'dispatched', 'Dispatched'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    vehicle = models.ForeignKey('fleet.Vehicle', on_delete=models.PROTECT, related_name='trips')
    driver = models.ForeignKey('drivers.Driver', on_delete=models.PROTECT, related_name='trips')
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2, help_text='Cargo weight in tons')
    distance = models.DecimalField(max_digits=10, decimal_places=2, help_text='Distance in km')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_trips')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Trip #{self.pk}: {self.source} → {self.destination}"

    @property
    def status_css_class(self):
        return f"status-{self.status.replace('_', '-')}"
