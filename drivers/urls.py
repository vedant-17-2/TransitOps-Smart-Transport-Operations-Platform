from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('', views.DriverListView.as_view(), name='driver_list'),
    path('add/', views.DriverCreateView.as_view(), name='driver_create'),
    path('<int:pk>/', views.DriverDetailView.as_view(), name='driver_detail'),
    path('<int:pk>/edit/', views.DriverUpdateView.as_view(), name='driver_update'),
    path('<int:pk>/delete/', views.DriverDeleteView.as_view(), name='driver_delete'),
    path('<int:pk>/update-status/', views.update_driver_status, name='driver_update_status'),
]
