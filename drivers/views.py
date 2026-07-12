from django.contrib.auth.mixins import LoginRequiredMixin
from core.mixins import RoleRequiredMixin, CSVExportMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Driver
from .forms import DriverForm

class DriverListView(LoginRequiredMixin, RoleRequiredMixin, CSVExportMixin, ListView):
    csv_filename = 'Driver_Report.csv'
    csv_export_fields = [('Name', 'name'), ('License Number', 'license_number'), ('Category', 'get_license_category_display'), ('Expiry Date', 'license_expiry'), ('Phone', 'phone'), ('Safety Score', 'safety_score'), ('Status', 'get_status_display')]
    allowed_roles = ['fleet_manager', 'dispatcher', 'safety_officer']
    model = Driver
    template_name = 'drivers/driver_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')
        category = self.request.GET.get('license_category')

        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(license_number__icontains=q))
        if status:
            queryset = queryset.filter(status=status)
        if category:
            queryset = queryset.filter(license_category=category)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Driver.LicenseCategory.choices
        context['statuses'] = Driver.Status.choices
        return context

class DriverCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    allowed_roles = ['fleet_manager']
    model = Driver
    form_class = DriverForm
    template_name = 'drivers/driver_form.html'
    success_url = reverse_lazy('drivers:driver_list')

    def form_valid(self, form):
        messages.success(self.request, 'Driver created successfully.')
        return super().form_valid(form)

class DriverUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    allowed_roles = ['fleet_manager']
    model = Driver
    form_class = DriverForm
    template_name = 'drivers/driver_form.html'
    success_url = reverse_lazy('drivers:driver_list')

    def get_form_class(self):
        form_class = super().get_form_class()
        form_class.Meta.fields = ['name', 'license_number', 'license_category', 'license_expiry', 'phone', 'safety_score', 'status', 'photo', 'license_document']
        return form_class

    def form_valid(self, form):
        messages.success(self.request, 'Driver updated successfully.')
        return super().form_valid(form)

class DriverDetailView(LoginRequiredMixin, RoleRequiredMixin, DetailView):
    allowed_roles = ['fleet_manager', 'dispatcher', 'safety_officer']
    model = Driver
    template_name = 'drivers/driver_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'trips'):
            context['recent_trips'] = self.object.trips.all()[:5]
        return context

class DriverDeleteView(LoginRequiredMixin, RoleRequiredMixin, DeleteView):
    allowed_roles = ['fleet_manager']
    model = Driver
    template_name = 'drivers/driver_confirm_delete.html'
    success_url = reverse_lazy('drivers:driver_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Driver deleted successfully.')
        return super().delete(request, *args, **kwargs)



import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
@require_POST
def update_driver_status(request, pk):
    if not request.user.is_superuser and getattr(request.user, 'profile', None) and request.user.profile.role not in ['fleet_manager', 'dispatcher', 'safety_officer']:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        
    try:
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status not in [choice[0] for choice in Driver.Status.choices]:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
            
        driver = get_object_or_404(Driver, pk=pk)
        driver.status = new_status
        driver.save(update_fields=['status'])
        
        return JsonResponse({'success': True, 'status': new_status})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
