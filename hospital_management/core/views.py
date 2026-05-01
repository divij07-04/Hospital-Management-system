from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, timedelta

from .forms import CuraLoginForm, UserProfileForm
from .models import Notification
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from pharmacy.models import Medicine
from billing.models import Invoice
from wards.models import Ward, Bed


def home_view(request):
    """Landing page — redirects to dashboard if logged in."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


def login_view(request):
    """Custom login view."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = CuraLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
    else:
        form = CuraLoginForm()
    return render(request, 'core/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Role-based dashboard with analytics widgets."""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    context = {
        'total_patients': Patient.objects.filter(is_active=True).count(),
        'total_doctors': Doctor.objects.filter(is_available=True).count(),
        'today_appointments': Appointment.objects.filter(date=today).count(),
        'pending_appointments': Appointment.objects.filter(status='pending').count(),
        'total_revenue': sum(
            inv.paid_amount for inv in Invoice.objects.filter(status='paid')
        ),
        'unpaid_invoices': Invoice.objects.filter(status='unpaid').count(),
        'available_beds': Bed.objects.filter(status='available').count(),
        'occupied_beds': Bed.objects.filter(status='occupied').count(),
        'low_stock_medicines': Medicine.objects.filter(
            quantity_in_stock__lte=models.F('reorder_level')
        ).count(),
        'recent_appointments': Appointment.objects.filter(
            date__gte=week_start
        ).select_related('patient', 'doctor')[:10],
        'recent_patients': Patient.objects.all()[:5],
        'notifications': Notification.objects.filter(
            user=request.user, is_read=False
        )[:5] if request.user.is_authenticated else [],
        # Chart data
        'weekly_appointments': _get_weekly_appointments(week_start),
        'status_distribution': _get_status_distribution(),
        'ward_occupancy': _get_ward_occupancy(),
    }
    return render(request, 'core/dashboard.html', context)


def _get_weekly_appointments(week_start):
    """Get appointment counts for current week for Chart.js."""
    data = []
    for i in range(7):
        day = week_start + timedelta(days=i)
        count = Appointment.objects.filter(date=day).count()
        data.append({'day': day.strftime('%a'), 'count': count})
    return data


def _get_status_distribution():
    """Appointment status distribution for pie chart."""
    statuses = ['pending', 'confirmed', 'in_progress', 'completed', 'cancelled']
    return [
        {'status': s.replace('_', ' ').title(), 'count': Appointment.objects.filter(status=s).count()}
        for s in statuses
    ]


def _get_ward_occupancy():
    """Ward occupancy data for bar chart."""
    wards = Ward.objects.all()
    return [
        {'name': w.name, 'occupied': w.occupied_beds, 'available': w.available_beds}
        for w in wards
    ]


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'core/profile.html', {'form': form})


@login_required
def mark_notification_read(request, pk):
    notif = Notification.objects.filter(pk=pk, user=request.user).first()
    if notif:
        notif.is_read = True
        notif.save()
    return redirect('dashboard')


# Need this import for F expression in dashboard
from django.db import models
