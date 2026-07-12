from django.urls import path
from . import views

app_name = 'fuel'

urlpatterns = [
    path('', views.FuelLogListView.as_view(), name='fuel_list'),
    path('add/', views.FuelLogCreateView.as_view(), name='fuel_create'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='expense_create'),
]
