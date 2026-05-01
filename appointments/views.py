from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment
from .forms import AppointmentForm, AppointmentStatusForm


@login_required
def appointment_list(request):
    status_filter = request.GET.get('status', '')
    appointments = Appointment.objects.select_related('patient', 'doctor', 'doctor__user').all()
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    return render(request, 'appointments/appointment_list.html', {
        'appointments': appointments, 'status_filter': status_filter,
    })


@login_required
def appointment_add(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('appointments:appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_form.html', {
        'form': form, 'title': 'Book New Appointment',
    })


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(
        Appointment.objects.select_related('patient', 'doctor', 'doctor__user'), pk=pk
    )
    has_prescription = hasattr(appointment, 'prescription')
    has_invoice = hasattr(appointment, 'invoice')
    return render(request, 'appointments/appointment_detail.html', {
        'appointment': appointment,
        'has_prescription': has_prescription,
        'has_invoice': has_invoice,
    })


@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment updated!')
            return redirect('appointments:appointment_detail', pk=pk)
    else:
        form = AppointmentStatusForm(instance=appointment)
    return render(request, 'appointments/appointment_update.html', {
        'form': form, 'appointment': appointment,
    })


@login_required
def appointment_cancel(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Appointment cancelled.')
        return redirect('appointments:appointment_list')
    return render(request, 'appointments/appointment_confirm_cancel.html', {
        'appointment': appointment,
    })
