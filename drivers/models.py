from django.db import models
from core.models import BaseModel
from datetime import date
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator, FileExtensionValidator

class Driver(BaseModel):
    class LicenseCategory(models.TextChoices):
        LMV = 'LMV', 'Light Motor Vehicle'
        HMV = 'HMV', 'Heavy Motor Vehicle'
        HTV = 'HTV', 'Heavy Transport Vehicle'
        HGMV = 'HGMV', 'Heavy Goods Motor Vehicle'

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'Available'
        ON_TRIP = 'on_trip', 'On Trip'
        ON_LEAVE = 'on_leave', 'On Leave'
        SUSPENDED = 'suspended', 'Suspended'

    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]+$',
                message="Name must contain only letters and spaces."
            )
        ]
    )
    license_number = models.CharField(
        max_length=20, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2}[0-9]{2}[0-9]{11}$',
                message="Enter a valid 15-character Indian driving license number (e.g., MH1420110062821)"
            )
        ]
    )
    license_category = models.CharField(max_length=10, choices=LicenseCategory.choices)
    license_expiry = models.DateField()
    phone = models.CharField(
        max_length=15, 
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message="Phone number must be exactly 10 digits."
            )
        ]
    )
    safety_score = models.PositiveIntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    photo = models.ImageField(
        upload_to='drivers/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    license_document = models.FileField(
        upload_to='licenses/', 
        blank=True, 
        null=True, 
        help_text="Upload driving license (Image or PDF)",
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.license_number})"

    @property
    def is_license_valid(self):
        return self.license_expiry >= date.today()

    @property
    def status_css_class(self):
        return f"status-{self.status.replace('_', '-')}"

    @property
    def safety_score_class(self):
        if self.safety_score >= 80:
            return 'safety-score-high'
        elif self.safety_score >= 50:
            return 'safety-score-medium'
        return 'safety-score-low'
