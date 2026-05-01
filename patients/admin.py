from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'first_name', 'last_name', 'gender', 'phone', 'registration_type', 'registered_on')
    list_filter = ('gender', 'blood_group', 'registration_type', 'is_active')
    search_fields = ('first_name', 'last_name', 'patient_id', 'phone')
    readonly_fields = ('patient_id', 'registered_on')
