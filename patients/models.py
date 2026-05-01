from django.db import models
from core.models import User


class Patient(models.Model):
    """Patient profile linked to User."""
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    )
    REG_TYPE_CHOICES = (
        ('OPD', 'Out-Patient'),
        ('IPD', 'In-Patient'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile', null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    registration_type = models.CharField(max_length=3, choices=REG_TYPE_CHOICES, default='OPD')
    # Medical info
    allergies = models.TextField(blank=True, help_text='Known allergies, comma-separated')
    chronic_conditions = models.TextField(blank=True, help_text='Chronic conditions like diabetes, hypertension, etc.')
    past_surgeries = models.TextField(blank=True)
    patient_id = models.CharField(max_length=20, unique=True, editable=False)
    registered_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-registered_on']

    def save(self, *args, **kwargs):
        if not self.patient_id:
            last = Patient.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.patient_id = f'CURA-P{num:05d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
