from django.db import models
from patients.models import Patient
from doctors.models import Doctor


class Appointment(models.Model):
    """Appointment between a patient and a doctor."""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    TIME_SLOT_CHOICES = (
        ('09:00', '09:00 AM'), ('09:30', '09:30 AM'),
        ('10:00', '10:00 AM'), ('10:30', '10:30 AM'),
        ('11:00', '11:00 AM'), ('11:30', '11:30 AM'),
        ('12:00', '12:00 PM'), ('12:30', '12:30 PM'),
        ('14:00', '02:00 PM'), ('14:30', '02:30 PM'),
        ('15:00', '03:00 PM'), ('15:30', '03:30 PM'),
        ('16:00', '04:00 PM'), ('16:30', '04:30 PM'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time_slot = models.CharField(max_length=5, choices=TIME_SLOT_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True, help_text='Reason for visit')
    diagnosis = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    appointment_id = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time_slot']
        unique_together = ['doctor', 'date', 'time_slot']

    def save(self, *args, **kwargs):
        if not self.appointment_id:
            last = Appointment.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.appointment_id = f'CURA-A{num:06d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.appointment_id} — {self.patient} with {self.doctor} on {self.date}"

    @property
    def status_color(self):
        colors = {
            'pending': 'warning',
            'confirmed': 'info',
            'in_progress': 'primary',
            'completed': 'success',
            'cancelled': 'danger',
        }
        return colors.get(self.status, 'secondary')
