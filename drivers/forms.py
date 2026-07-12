from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'license_number', 'license_category', 'license_expiry', 'phone', 'safety_score', 'photo', 'license_document']
        widgets = {
            'license_expiry': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_license_expiry(self):
        expiry = self.cleaned_data.get('license_expiry')
        import datetime
        if expiry and expiry < datetime.date.today():
            raise forms.ValidationError("License has already expired.")
        return expiry

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and hasattr(photo, 'size'):
            if photo.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Photo file size cannot exceed 5MB.")
        return photo

    def clean_license_document(self):
        doc = self.cleaned_data.get('license_document')
        if doc and hasattr(doc, 'size'):
            if doc.size > 5 * 1024 * 1024:
                raise forms.ValidationError("License document file size cannot exceed 5MB.")
        return doc

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('phone', css_class='col-md-6'),
            ),
            Row(
                Column('license_number', css_class='col-md-4'),
                Column('license_category', css_class='col-md-4'),
                Column('license_expiry', css_class='col-md-4'),
            ),
            Row(
                Column('safety_score', css_class='col-md-4'),
                Column('photo', css_class='col-md-4'),
                Column('license_document', css_class='col-md-4'),
            ),
            Submit('submit', 'Save Driver', css_class='btn-primary mt-3')
        )
