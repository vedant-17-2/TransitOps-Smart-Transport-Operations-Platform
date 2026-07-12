from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import RoleRequiredMixin, CSVExportMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import FuelLog, Expense
from .forms import FuelLogForm, ExpenseForm
from fleet.models import Vehicle

class FuelLogListView(LoginRequiredMixin, RoleRequiredMixin, CSVExportMixin, ListView):
    csv_filename = 'Fuel_Log_Report.csv'
    csv_export_fields = [('Date', 'date'), ('Vehicle', 'vehicle.registration_number'), ('Trip', 'trip.trip_number'), ('Quantity (L)', 'quantity_liters'), ('Cost', 'total_cost')]
    allowed_roles = ['fleet_manager', 'financial_analyst']
    model = FuelLog
    template_name = 'fuel/fuel_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('vehicle')
        vehicle_id = self.request.GET.get('vehicle')
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.all()
        return context

class FuelLogCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ['fleet_manager']
    model = FuelLog
    form_class = FuelLogForm
    template_name = 'fuel/fuel_form.html'
    success_url = reverse_lazy('fuel:fuel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Fuel log added successfully.')
        return super().form_valid(form)

class ExpenseListView(LoginRequiredMixin, RoleRequiredMixin, CSVExportMixin, ListView):
    csv_filename = 'Expense_Report.csv'
    csv_export_fields = [('Date', 'date'), ('Vehicle', 'vehicle.registration_number'), ('Type', 'get_expense_type_display'), ('Amount', 'amount'), ('Description', 'description')]
    allowed_roles = ['fleet_manager', 'financial_analyst']
    model = Expense
    template_name = 'fuel/expense_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('vehicle')
        vehicle_id = self.request.GET.get('vehicle')
        expense_type = self.request.GET.get('expense_type')
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        if expense_type:
            queryset = queryset.filter(expense_type=expense_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.all()
        context['expense_types'] = Expense.ExpenseType.choices
        
        # Calculate total expenses this month
        today = timezone.now().date()
        month_start = today.replace(day=1)
        total_expenses = Expense.objects.filter(date__gte=month_start).aggregate(total=Sum('amount'))['total'] or 0
        context['total_expenses'] = total_expenses
        
        return context

class ExpenseCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ['fleet_manager']
    model = Expense
    form_class = ExpenseForm
    template_name = 'fuel/expense_form.html'
    success_url = reverse_lazy('fuel:expense_list')

    def form_valid(self, form):
        messages.success(self.request, 'Expense logged successfully.')
        return super().form_valid(form)


