from django.urls import path
from . import views

app_name = 'wards'

urlpatterns = [
    path('', views.ward_list, name='ward_list'),
    path('add/', views.ward_add, name='ward_add'),
    path('<int:pk>/', views.ward_detail, name='ward_detail'),
    path('bed/<int:pk>/admit/', views.bed_admit, name='bed_admit'),
    path('bed/<int:pk>/discharge/', views.bed_discharge, name='bed_discharge'),
]
