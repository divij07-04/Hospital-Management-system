from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'date', 'time_slot', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('appointment_id', 'patient__first_name', 'doctor__user__first_name')
    readonly_fields = ('appointment_id',)
