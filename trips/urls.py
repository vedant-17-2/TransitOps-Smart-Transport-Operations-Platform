from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.TripListView.as_view(), name='trip_list'),
    path('add/', views.TripCreateView.as_view(), name='trip_create'),
    path('<int:pk>/', views.TripDetailView.as_view(), name='trip_detail'),
    path('<int:pk>/complete/', views.complete_trip, name='trip_complete'),
    path('<int:pk>/cancel/', views.cancel_trip, name='trip_cancel'),
]
