from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Vehicle

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['registration_number', 'vehicle_name', 'vehicle_type', 'capacity', 'current_odometer', 'acquisition_cost', 'insurance_expiry', 'rc_expiry', 'image']
        widgets = {
            'insurance_expiry': forms.DateInput(attrs={'type': 'date'}),
            'rc_expiry': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_registration_number(self):
        reg_num = self.cleaned_data.get('registration_number', '')
        if reg_num:
            reg_num = reg_num.replace(" ", "").upper()
        return reg_num

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('registration_number', css_class='col-md-6'),
                Column('vehicle_name', css_class='col-md-6'),
            ),
            Row(
                Column('vehicle_type', css_class='col-md-4'),
                Column('capacity', css_class='col-md-4'),
                Column('current_odometer', css_class='col-md-4'),
            ),
            Row(
                Column('acquisition_cost', css_class='col-md-4'),
                Column('insurance_expiry', css_class='col-md-4'),
                Column('rc_expiry', css_class='col-md-4'),
            ),
            Row(
                Column('image', css_class='col-md-12'),
            ),
            Submit('submit', 'Save Vehicle', css_class='btn-primary mt-3')
        )
