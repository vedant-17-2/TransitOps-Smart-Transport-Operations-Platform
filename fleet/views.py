from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Vehicle
from .forms import VehicleForm

class VehicleListView(LoginRequiredMixin, ListView):
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

class VehicleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'fleet/vehicle_form.html'
    success_url = reverse_lazy('fleet:vehicle_list')

    def test_func(self):
        return self.request.user.is_superuser or (hasattr(self.request.user, 'profile') and self.request.user.profile.role in ['fleet_manager'])

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle created successfully.')
        return super().form_valid(form)

class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'fleet/vehicle_form.html'
    success_url = reverse_lazy('fleet:vehicle_list')

    def test_func(self):
        return self.request.user.is_superuser or (hasattr(self.request.user, 'profile') and self.request.user.profile.role in ['fleet_manager'])

    def get_form_class(self):
        # We want to be able to edit status during update
        form_class = super().get_form_class()
        form_class.Meta.fields = ['registration_number', 'vehicle_name', 'vehicle_type', 'capacity', 'current_odometer', 'acquisition_cost', 'status', 'image']
        return form_class

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle updated successfully.')
        return super().form_valid(form)

class VehicleDetailView(LoginRequiredMixin, DetailView):
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

class VehicleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vehicle
    template_name = 'fleet/vehicle_confirm_delete.html'
    success_url = reverse_lazy('fleet:vehicle_list')

    def test_func(self):
        return self.request.user.is_superuser or (hasattr(self.request.user, 'profile') and self.request.user.profile.role in ['fleet_manager'])

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Vehicle deleted successfully.')
        return super().delete(request, *args, **kwargs)
