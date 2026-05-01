from django.contrib import admin
from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'appointment', 'total_amount', 'discount', 'paid_amount', 'status')
    list_filter = ('status',)
    search_fields = ('invoice_id',)
    readonly_fields = ('invoice_id',)
    inlines = [InvoiceItemInline]
