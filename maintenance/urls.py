from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.MaintenanceListView.as_view(), name='maintenance_list'),
    path('add/', views.MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('<int:pk>/complete/', views.complete_maintenance, name='maintenance_complete'),
]
