from django.contrib import admin
from .models import Ward, Bed


class BedInline(admin.TabularInline):
    model = Bed
    extra = 1


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward_type', 'floor', 'capacity', 'charge_per_day')
    list_filter = ('ward_type',)
    inlines = [BedInline]


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('ward', 'bed_number', 'status', 'patient')
    list_filter = ('status', 'ward')
