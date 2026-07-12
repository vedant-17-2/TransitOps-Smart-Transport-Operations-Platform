from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import MaintenanceRecord
from fleet.models import Vehicle

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['vehicle', 'maintenance_type', 'description', 'cost', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude retired vehicles
        self.fields['vehicle'].queryset = Vehicle.objects.exclude(status=Vehicle.Status.RETIRED)
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('vehicle', css_class='col-md-6'),
                Column('maintenance_type', css_class='col-md-6'),
            ),
            Row(
                Column('date', css_class='col-md-6'),
                Column('cost', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Record', css_class='btn-primary mt-3')
        )
