from django.db import models
from patients.models import Patient


class Ward(models.Model):
    """Hospital ward / department."""
    WARD_TYPE_CHOICES = (
        ('general', 'General Ward'),
        ('semi_private', 'Semi-Private'),
        ('private', 'Private Room'),
        ('icu', 'ICU'),
        ('nicu', 'NICU'),
        ('ot', 'Operation Theatre'),
    )
    name = models.CharField(max_length=100)
    ward_type = models.CharField(max_length=20, choices=WARD_TYPE_CHOICES)
    floor = models.PositiveIntegerField(default=1)
    capacity = models.PositiveIntegerField(default=10)
    charge_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_ward_type_display()})"

    @property
    def occupied_beds(self):
        return self.beds.filter(status='occupied').count()

    @property
    def available_beds(self):
        return self.beds.filter(status='available').count()

    @property
    def occupancy_percentage(self):
        total = self.beds.count()
        if total == 0:
            return 0
        return round((self.occupied_beds / total) * 100)


class Bed(models.Model):
    """Individual bed in a ward."""
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
    )
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='bed')
    admitted_on = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['ward', 'bed_number']
        unique_together = ['ward', 'bed_number']

    def __str__(self):
        return f"{self.ward.name} — Bed {self.bed_number}"

    @property
    def status_color(self):
        colors = {
            'available': 'success',
            'occupied': 'danger',
            'reserved': 'warning',
            'maintenance': 'secondary',
        }
        return colors.get(self.status, 'secondary')
