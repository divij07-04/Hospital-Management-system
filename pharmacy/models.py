from django.db import models
from appointments.models import Appointment


class Medicine(models.Model):
    """Medicine inventory item."""
    CATEGORY_CHOICES = (
        ('tablet', 'Tablet'),
        ('capsule', 'Capsule'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('ointment', 'Ointment'),
        ('drops', 'Drops'),
        ('inhaler', 'Inhaler'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    manufacturer = models.CharField(max_length=200, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)
    expiry_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.reorder_level

    @property
    def is_expired(self):
        if self.expiry_date:
            from datetime import date
            return self.expiry_date <= date.today()
        return False


class Prescription(models.Model):
    """Prescription linked to an appointment."""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    notes = models.TextField(blank=True, help_text='Additional instructions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.appointment.appointment_id}"


class PrescriptionItem(models.Model):
    """Individual medicine in a prescription."""
    DOSAGE_CHOICES = (
        ('1-0-0', 'Morning only'),
        ('0-1-0', 'Afternoon only'),
        ('0-0-1', 'Night only'),
        ('1-1-0', 'Morning & Afternoon'),
        ('1-0-1', 'Morning & Night'),
        ('0-1-1', 'Afternoon & Night'),
        ('1-1-1', 'Three times a day'),
        ('sos', 'SOS / As needed'),
    )
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=10, choices=DOSAGE_CHOICES, default='1-1-1')
    duration_days = models.PositiveIntegerField(default=5)
    quantity = models.PositiveIntegerField(default=1)
    instructions = models.CharField(max_length=200, blank=True, help_text='e.g. After food')

    def __str__(self):
        return f"{self.medicine.name} — {self.dosage} for {self.duration_days} days"
