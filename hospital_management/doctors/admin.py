from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('doctor_id', 'user', 'specialization', 'consultation_fee', 'is_available')
    list_filter = ('specialization', 'is_available')
    search_fields = ('user__first_name', 'user__last_name', 'doctor_id')
    readonly_fields = ('doctor_id',)
