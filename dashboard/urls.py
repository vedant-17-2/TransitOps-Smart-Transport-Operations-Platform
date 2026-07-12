from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('api/vehicle-status/', views.api_vehicle_status, name='api_vehicle_status'),
    path('api/trip-stats/', views.api_trip_stats, name='api_trip_stats'),
]
