from django.db import models
from core.models import BaseModel
from django.core.validators import RegexValidator, MinValueValidator
from django.core.files.base import ContentFile
from io import BytesIO
import qrcode

class Vehicle(BaseModel):
    class VehicleType(models.TextChoices):
        TRUCK = 'truck', 'Truck'
        VAN = 'van', 'Van'
        BUS = 'bus', 'Bus'
        PICKUP = 'pickup', 'Pickup'
        TANKER = 'tanker', 'Tanker'

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        ON_TRIP = 'on_trip', 'On Trip'
        IN_SHOP = 'in_shop', 'In Shop'
        RETIRED = 'retired', 'Retired'

    registration_number = models.CharField(
        max_length=20, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$', 
                message="Enter a valid Indian vehicle registration number (e.g. MH01AB1234)"
            )
        ]
    )
    vehicle_name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=VehicleType.choices, default=VehicleType.TRUCK)
    capacity = models.DecimalField(
        max_digits=10, decimal_places=2, help_text='Max load in tons', 
        validators=[MinValueValidator(0.1)]
    )
    current_odometer = models.PositiveIntegerField(
        default=0, help_text='Odometer in km',
        validators=[MinValueValidator(0)]
    )
    acquisition_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    insurance_expiry = models.DateField(null=True, blank=True)
    rc_expiry = models.DateField(null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.registration_number} - {self.vehicle_name}"

    @property
    def status_css_class(self):
        return f"status-{self.status.replace('_', '-')}"

    def save(self, *args, **kwargs):
        # Save first to ensure we have a PK
        super().save(*args, **kwargs)
        
        # Generate QR code if it doesn't exist
        if not self.qr_code:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            # Encode basic details, maybe a URL path for the detail view
            qr_data = f"Vehicle: {self.registration_number}\nURL: /fleet/{self.pk}/"
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            
            file_name = f'qr_vehicle_{self.pk}.png'
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
            
            # Save again just to update the qr_code field
            super().save(update_fields=['qr_code'])
