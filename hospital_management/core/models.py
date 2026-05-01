from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role-based access for CURA."""
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('receptionist', 'Receptionist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='patient')
    phone = models.CharField(max_length=15, blank=True)
    profile_pic = models.URLField(blank=True, help_text='Profile picture URL')
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_doctor(self):
        return self.role == 'doctor'

    @property
    def is_patient(self):
        return self.role == 'patient'

    @property
    def is_receptionist(self):
        return self.role == 'receptionist'


class Notification(models.Model):
    """Simple notification system."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.CharField(max_length=50, default='bi-bell')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
