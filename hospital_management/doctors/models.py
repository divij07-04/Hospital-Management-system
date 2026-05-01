from django.db import models
from core.models import User


class Doctor(models.Model):
    """Doctor profile linked to User."""
    SPECIALIZATION_CHOICES = (
        ('general', 'General Medicine'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('ent', 'ENT'),
        ('ophthalmology', 'Ophthalmology'),
        ('gynecology', 'Gynecology'),
        ('psychiatry', 'Psychiatry'),
        ('surgery', 'General Surgery'),
        ('radiology', 'Radiology'),
    )
    DAY_CHOICES = (
        ('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'),
        ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=30, choices=SPECIALIZATION_CHOICES)
    qualification = models.CharField(max_length=200, help_text='e.g. MBBS, MD, MS')
    experience_years = models.PositiveIntegerField(default=0)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500)
    available_days = models.CharField(max_length=100, blank=True, help_text='Comma-separated: mon,tue,wed')
    available_from = models.TimeField(default='09:00')
    available_to = models.TimeField(default='17:00')
    doctor_id = models.CharField(max_length=20, unique=True, editable=False)
    bio = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['user__first_name']

    def save(self, *args, **kwargs):
        if not self.doctor_id:
            last = Doctor.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.doctor_id = f'CURA-D{num:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} — {self.get_specialization_display()}"

    @property
    def available_days_list(self):
        if self.available_days:
            return [d.strip() for d in self.available_days.split(',')]
        return []
