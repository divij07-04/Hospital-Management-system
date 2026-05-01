from django.contrib import admin
from .models import Medicine, Prescription, PrescriptionItem


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity_in_stock', 'expiry_date', 'is_low_stock')
    list_filter = ('category',)
    search_fields = ('name', 'generic_name')


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'created_at')
    inlines = [PrescriptionItemInline]
