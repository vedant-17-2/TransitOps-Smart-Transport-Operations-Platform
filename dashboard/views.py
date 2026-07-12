import json
from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum, Q, Avg
from django.db.models.functions import TruncMonth
from fleet.models import Vehicle
from drivers.models import Driver
from trips.models import Trip
from maintenance.models import MaintenanceRecord
from fuel.models import FuelLog, Expense

@login_required
def dashboard_view(request):
    today = date.today()
    month_start = today.replace(day=1)
    
    # Vehicle KPIs
    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE).count()
    on_trip_vehicles = Vehicle.objects.filter(status=Vehicle.Status.ON_TRIP).count()
    in_shop_vehicles = Vehicle.objects.filter(status=Vehicle.Status.IN_SHOP).count()
    
    # Driver KPIs
    total_drivers = Driver.objects.count()
    available_drivers = Driver.objects.filter(status=Driver.Status.AVAILABLE).count()
    on_duty_drivers = Driver.objects.filter(status=Driver.Status.ON_TRIP).count()
    
    # Trip KPIs
    active_trips = Trip.objects.filter(status__in=[Trip.Status.DISPATCHED, Trip.Status.IN_PROGRESS]).count()
    pending_trips = Trip.objects.filter(status=Trip.Status.PENDING).count()
    completed_trips_month = Trip.objects.filter(status=Trip.Status.COMPLETED, end_date__date__gte=month_start).count()
    
    # Fleet Utilization
    fleet_utilization = round((on_trip_vehicles / total_vehicles * 100), 1) if total_vehicles > 0 else 0
    
    # Costs this month
    total_fuel_cost_month = FuelLog.objects.filter(date__gte=month_start).aggregate(total=Sum('cost'))['total'] or 0
    total_maint_cost_month = MaintenanceRecord.objects.filter(date__gte=month_start).aggregate(total=Sum('cost'))['total'] or 0
    
    # Recent trips
    recent_trips = Trip.objects.select_related('vehicle', 'driver').all()[:10]
    
    # Chart data: Vehicle Status
    vehicle_status_data = {
        'labels': ['Available', 'On Trip', 'In Shop', 'Retired'],
        'data': [available_vehicles, on_trip_vehicles, in_shop_vehicles, Vehicle.objects.filter(status=Vehicle.Status.RETIRED).count()],
        'colors': ['#059669', '#1a56db', '#d97706', '#dc2626']
    }
    
    # Chart data: Monthly Trips (last 6 months)
    six_months_ago = today - timedelta(days=180)
    monthly_trips = Trip.objects.filter(start_date__date__gte=six_months_ago).annotate(month=TruncMonth('start_date')).values('month').annotate(count=Count('id')).order_by('month')
    monthly_trips_data = {
        'labels': [item['month'].strftime('%b %Y') for item in monthly_trips] if monthly_trips else [],
        'data': [item['count'] for item in monthly_trips] if monthly_trips else []
    }
    
    context = {
        'total_vehicles': total_vehicles, 'available_vehicles': available_vehicles,
        'in_shop_vehicles': in_shop_vehicles, 'active_trips': active_trips,
        'on_duty_drivers': on_duty_drivers, 'fleet_utilization': fleet_utilization,
        'pending_trips': pending_trips, 'completed_trips_month': completed_trips_month,
        'total_fuel_cost_month': total_fuel_cost_month, 'total_maint_cost_month': total_maint_cost_month,
        'recent_trips': recent_trips,
        'vehicle_status_data': vehicle_status_data,
        'monthly_trips_data': monthly_trips_data,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def analytics_view(request):
    today = date.today()
    # Total stats
    total_trips = Trip.objects.count()
    total_fuel_cost = FuelLog.objects.aggregate(t=Sum('cost'))['t'] or 0
    total_maint_cost = MaintenanceRecord.objects.aggregate(t=Sum('cost'))['t'] or 0
    total_vehicles = Vehicle.objects.count()
    on_trip = Vehicle.objects.filter(status=Vehicle.Status.ON_TRIP).count()
    avg_utilization = round((on_trip / total_vehicles * 100), 1) if total_vehicles > 0 else 0
    
    # Fuel trend (6 months)
    six_months_ago = today - timedelta(days=180)
    fuel_trend = FuelLog.objects.filter(date__gte=six_months_ago).annotate(month=TruncMonth('date')).values('month').annotate(total=Sum('cost')).order_by('month')
    fuel_trend_data = {'labels': [f['month'].strftime('%b %Y') for f in fuel_trend], 'data': [float(f['total']) for f in fuel_trend]}
    
    # Expense breakdown
    expense_breakdown = Expense.objects.values('expense_type').annotate(total=Sum('amount')).order_by('-total')
    expense_data = {'labels': [e['expense_type'].replace('_',' ').title() for e in expense_breakdown], 'data': [float(e['total']) for e in expense_breakdown]}
    
    # Trip volume 12 months
    year_ago = today - timedelta(days=365)
    trip_volume = Trip.objects.filter(start_date__date__gte=year_ago).annotate(month=TruncMonth('start_date')).values('month').annotate(count=Count('id')).order_by('month')
    trip_volume_data = {'labels': [t['month'].strftime('%b %Y') for t in trip_volume], 'data': [t['count'] for t in trip_volume]}
    
    # Top vehicles
    top_vehicles = Vehicle.objects.annotate(trip_count=Count('trips')).order_by('-trip_count')[:5]
    top_vehicles_data = {'labels': [v.registration_number for v in top_vehicles], 'data': [v.trip_count for v in top_vehicles]}
    
    # Top drivers
    top_drivers = Driver.objects.annotate(trip_count=Count('trips')).order_by('-trip_count')[:5]
    top_drivers_data = {'labels': [d.name for d in top_drivers], 'data': [d.trip_count for d in top_drivers]}
    
    context = {
        'total_trips': total_trips, 'total_fuel_cost': total_fuel_cost,
        'total_maint_cost': total_maint_cost, 'avg_utilization': avg_utilization,
        'fuel_trend_data': fuel_trend_data, 'expense_data': expense_data,
        'trip_volume_data': trip_volume_data,
        'top_vehicles_data': top_vehicles_data, 'top_drivers_data': top_drivers_data,
    }
    return render(request, 'dashboard/analytics.html', context)

@login_required
def api_vehicle_status(request):
    data = {s[0]: Vehicle.objects.filter(status=s[0]).count() for s in Vehicle.Status.choices}
    return JsonResponse(data)

@login_required
def api_trip_stats(request):
    data = {s[0]: Trip.objects.filter(status=s[0]).count() for s in Trip.Status.choices}
    return JsonResponse(data)
