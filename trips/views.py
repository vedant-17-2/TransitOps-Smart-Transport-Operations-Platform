from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Trip
from .forms import TripForm
from fleet.models import Vehicle
from drivers.models import Driver

class TripListView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'trips/trip_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        status = self.request.GET.get('status')

        if q:
            queryset = queryset.filter(Q(source__icontains=q) | Q(destination__icontains=q))
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Trip.Status.choices
        return context

class TripCreateView(LoginRequiredMixin, CreateView):
    model = Trip
    form_class = TripForm
    template_name = 'trips/trip_form.html'
    success_url = reverse_lazy('trips:trip_list')

    def form_valid(self, form):
        # Set created_by
        form.instance.created_by = self.request.user
        form.instance.status = Trip.Status.DISPATCHED
        
        # Save trip
        response = super().form_valid(form)
        
        # Update vehicle and driver status
        vehicle = self.object.vehicle
        vehicle.status = Vehicle.Status.ON_TRIP
        vehicle.save()
        
        driver = self.object.driver
        driver.status = Driver.Status.ON_TRIP
        driver.save()
        
        messages.success(self.request, 'Trip dispatched successfully.')
        return response

class TripDetailView(LoginRequiredMixin, DetailView):
    model = Trip
    template_name = 'trips/trip_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'fuel_logs'):
            context['fuel_logs'] = self.object.fuel_logs.all()
        return context

@login_required
def complete_trip(request, pk):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, pk=pk)
        if trip.status in [Trip.Status.DISPATCHED, Trip.Status.IN_PROGRESS]:
            trip.status = Trip.Status.COMPLETED
            trip.end_date = timezone.now()
            trip.save()
            
            # Update vehicle
            vehicle = trip.vehicle
            vehicle.status = Vehicle.Status.AVAILABLE
            vehicle.current_odometer += trip.distance
            vehicle.save()
            
            # Update driver
            driver = trip.driver
            driver.status = Driver.Status.AVAILABLE
            driver.save()
            
            messages.success(request, 'Trip marked as completed.')
        else:
            messages.error(request, 'Only dispatched or in-progress trips can be completed.')
    return redirect('trips:trip_detail', pk=pk)

@login_required
def cancel_trip(request, pk):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, pk=pk)
        if trip.status in [Trip.Status.PENDING, Trip.Status.DISPATCHED, Trip.Status.IN_PROGRESS]:
            trip.status = Trip.Status.CANCELLED
            trip.save()
            
            # Revert vehicle
            vehicle = trip.vehicle
            vehicle.status = Vehicle.Status.AVAILABLE
            vehicle.save()
            
            # Revert driver
            driver = trip.driver
            driver.status = Driver.Status.AVAILABLE
            driver.save()
            
            messages.success(request, 'Trip has been cancelled.')
        else:
            messages.error(request, 'Cannot cancel a completed trip.')
    return redirect('trips:trip_list')
