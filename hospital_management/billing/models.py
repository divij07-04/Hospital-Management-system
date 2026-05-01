from django.db import models
from appointments.models import Appointment


class Invoice(models.Model):
    """Invoice generated for an appointment."""
    STATUS_CHOICES = (
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Paid'),
    )
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='invoice')
    invoice_id = models.CharField(max_length=20, unique=True, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last = Invoice.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.invoice_id = f'CURA-INV{num:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_id} — ₹{self.net_amount}"

    @property
    def net_amount(self):
        return self.total_amount - self.discount

    @property
    def due_amount(self):
        return self.net_amount - self.paid_amount

    @property
    def status_color(self):
        colors = {'unpaid': 'danger', 'partial': 'warning', 'paid': 'success'}
        return colors.get(self.status, 'secondary')


class InvoiceItem(models.Model):
    """Line item within an invoice."""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=300)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.description} — ₹{self.line_total}"
