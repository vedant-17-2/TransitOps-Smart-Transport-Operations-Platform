from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import RoleRequiredMixin, CSVExportMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Vehicle
from .forms import VehicleForm

class VehicleListView(LoginRequiredMixin, RoleRequiredMixin, CSVExportMixin, ListView):
    csv_filename = 'Vehicle_Report.csv'
    csv_export_fields = [('Registration Number', 'registration_number'), ('Vehicle Name', 'vehicle_name'), ('Type', 'get_vehicle_type_display'), ('Capacity (Tons)', 'capacity'), ('Odometer (km)', 'current_odometer'), ('Cost', 'acquisition_cost'), ('Status', 'get_status_display')]
    allowed_roles = ['fleet_manager', 'dispatcher']
    model = Vehicle
    template_name = 'fleet/vehicle_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        vehicle_type = self.request.GET.get('vehicle_type')

        if q:
            queryset = queryset.filter(Q(registration_number__icontains=q) | Q(vehicle_name__icontains=q))
        if status:
            queryset = queryset.filter(status=status)
        if vehicle_type:
            queryset = queryset.filter(vehicle_type=vehicle_type)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle_types'] = Vehicle.VehicleType.choices
        context['statuses'] = Vehicle.Status.choices
        return context

class VehicleCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ['fleet_manager']
    model = Vehicle
    form_class = VehicleForm
    template_name = 'fleet/vehicle_form.html'
    success_url = reverse_lazy('fleet:vehicle_list')

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle created successfully.')
        return super().form_valid(form)

class VehicleUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ['fleet_manager']
    model = Vehicle
    form_class = VehicleForm
    template_name = 'fleet/vehicle_form.html'
    success_url = reverse_lazy('fleet:vehicle_list')

    def get_form_class(self):
        # We want to be able to edit status during update
        form_class = super().get_form_class()
        form_class.Meta.fields = ['registration_number', 'vehicle_name', 'vehicle_type', 'capacity', 'current_odometer', 'acquisition_cost', 'status', 'image']
        return form_class

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle updated successfully.')
        return super().form_valid(form)

class VehicleDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    allowed_roles = ['fleet_manager', 'dispatcher']
    model = Vehicle
    template_name = 'fleet/vehicle_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Using hasattr to avoid errors if trips/maintenance app isn't fully created yet, though related_name handles it when they exist
        if hasattr(self.object, 'trips'):
            context['recent_trips'] = self.object.trips.all()[:5]
        if hasattr(self.object, 'maintenance_records'):
            context['recent_maintenance'] = self.object.maintenance_records.all()[:5]
        return context

class VehicleDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ['fleet_manager']
    model = Vehicle
    template_name = 'fleet/vehicle_confirm_delete.html'
    success_url = reverse_lazy('fleet:vehicle_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Vehicle deleted successfully.')
        return super().delete(request, *args, **kwargs)



import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def update_vehicle_status(request, pk):
    if not request.user.is_superuser and getattr(request.user, 'profile', None) and request.user.profile.role not in ['fleet_manager', 'dispatcher']:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status not in [choice[0] for choice in Vehicle.Status.choices]:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
            
        vehicle = get_object_or_404(Vehicle, pk=pk)
        vehicle.status = new_status
        vehicle.save(update_fields=['status'])
        
        return JsonResponse({'success': True, 'status': new_status})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
