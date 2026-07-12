from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Trip
from fleet.models import Vehicle
from drivers.models import Driver

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['vehicle', 'driver', 'source', 'destination', 'cargo_weight', 'distance', 'start_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show available vehicles and drivers
        self.fields['vehicle'].queryset = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE)
        self.fields['driver'].queryset = Driver.objects.filter(status=Driver.Status.AVAILABLE)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('vehicle', css_class='col-md-6'),
                Column('driver', css_class='col-md-6'),
            ),
            Row(
                Column('source', css_class='col-md-6'),
                Column('destination', css_class='col-md-6'),
            ),
            Row(
                Column('cargo_weight', css_class='col-md-4'),
                Column('distance', css_class='col-md-4'),
                Column('start_date', css_class='col-md-4'),
            ),
            Submit('submit', 'Dispatch Trip', css_class='btn-primary mt-3')
        )

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        driver = cleaned_data.get('driver')
        cargo_weight = cleaned_data.get('cargo_weight')
        errors = []

        if vehicle:
            if vehicle.status != Vehicle.Status.AVAILABLE:
                errors.append(f"Vehicle is currently {vehicle.get_status_display()}")
            if vehicle.status in [Vehicle.Status.IN_SHOP, Vehicle.Status.RETIRED]:
                errors.append("Vehicle cannot be dispatched (In Shop or Retired)")
            if cargo_weight and cargo_weight > vehicle.capacity:
                errors.append(f"Cargo weight {cargo_weight}t exceeds vehicle capacity of {vehicle.capacity}t")

        if driver:
            if driver.status != Driver.Status.AVAILABLE:
                errors.append(f"Driver is currently {driver.get_status_display()}")
            if driver.status == Driver.Status.SUSPENDED:
                errors.append("Driver is suspended and cannot be dispatched")
            if not driver.is_license_valid:
                errors.append(f"Driver's license expired on {driver.license_expiry}")

        if errors:
            raise ValidationError(errors)
            
        return cleaned_data
