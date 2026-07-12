from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import FuelLog, Expense

class FuelLogForm(forms.ModelForm):
    class Meta:
        model = FuelLog
        fields = ['vehicle', 'trip', 'fuel_quantity', 'cost', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('vehicle', css_class='col-md-6'),
                Column('trip', css_class='col-md-6'),
            ),
            Row(
                Column('fuel_quantity', css_class='col-md-4'),
                Column('cost', css_class='col-md-4'),
                Column('date', css_class='col-md-4'),
            ),
            Submit('submit', 'Save Fuel Log', css_class='btn-primary mt-3')
        )

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['vehicle', 'expense_type', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('vehicle', css_class='col-md-6'),
                Column('expense_type', css_class='col-md-6'),
            ),
            Row(
                Column('amount', css_class='col-md-6'),
                Column('date', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', 'Save Expense', css_class='btn-primary mt-3')
        )
