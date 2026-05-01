from django.urls import path
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('add/', views.medicine_add, name='medicine_add'),
    path('<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    path('prescription/create/<int:appointment_pk>/', views.prescription_create, name='prescription_create'),
    path('prescription/<int:pk>/', views.prescription_detail, name='prescription_detail'),
]
