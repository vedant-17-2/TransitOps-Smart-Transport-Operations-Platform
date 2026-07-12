from django.urls import path
from . import views

app_name = 'fleet'

urlpatterns = [
    path('', views.VehicleListView.as_view(), name='vehicle_list'),
    path('add/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('<int:pk>/edit/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    path('<int:pk>/update-status/', views.update_vehicle_status, name='vehicle_update_status'),
]
