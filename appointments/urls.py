from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.appointment_list, name='appointment_list'),
    path('add/', views.appointment_add, name='appointment_add'),
    path('<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('<int:pk>/update/', views.appointment_update, name='appointment_update'),
    path('<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
]
