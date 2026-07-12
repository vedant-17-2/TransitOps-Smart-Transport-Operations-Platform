from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import RoleRequiredMixin, role_required, CSVExportMixin, CSVExportMixin
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from .models import MaintenanceRecord
from .forms import MaintenanceForm
from fleet.models import Vehicle

class MaintenanceListView(LoginRequiredMixin, RoleRequiredMixin, CSVExportMixin, ListView):
    csv_filename = 'Maintenance_Report.csv'
    csv_export_fields = [('Date', 'date'), ('Vehicle', 'vehicle.registration_number'), ('Type', 'get_maintenance_type_display'), ('Cost', 'cost'), ('Status', 'get_status_display')]
    allowed_roles = ['fleet_manager', 'financial_analyst']
    model = MaintenanceRecord
    template_name = 'maintenance/maintenance_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('vehicle')
        vehicle_id = self.request.GET.get('vehicle')
        status = self.request.GET.get('status')

        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.exclude(status=Vehicle.Status.RETIRED)
        context['statuses'] = MaintenanceRecord.Status.choices
        return context

class MaintenanceCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ['fleet_manager']
    model = MaintenanceRecord
    form_class = MaintenanceForm
    template_name = 'maintenance/maintenance_form.html'
    success_url = reverse_lazy('maintenance:maintenance_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Change vehicle status
        vehicle = self.object.vehicle
        vehicle.status = Vehicle.Status.IN_SHOP
        vehicle.save()
        
        messages.success(self.request, 'Maintenance record created. Vehicle status changed to In Shop.')
        return response

@login_required
@role_required(['fleet_manager'])
def complete_maintenance(request, pk):
    if request.method == 'POST':
        record = get_object_or_404(MaintenanceRecord, pk=pk)
        if record.status == MaintenanceRecord.Status.OPEN:
            record.status = MaintenanceRecord.Status.COMPLETED
            record.completed_date = timezone.now().date()
            record.save()
            
            # Change vehicle status back if it was in_shop
            vehicle = record.vehicle
            if vehicle.status == Vehicle.Status.IN_SHOP:
                vehicle.status = Vehicle.Status.AVAILABLE
                vehicle.save()
            
            messages.success(request, 'Maintenance marked as completed. Vehicle is now available.')
    return redirect('maintenance:maintenance_list')


