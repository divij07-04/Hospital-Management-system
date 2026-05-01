from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Patient
from .forms import PatientForm


@login_required
def patient_list(request):
    query = request.GET.get('q', '')
    reg_type = request.GET.get('type', '')
    patients = Patient.objects.filter(is_active=True)
    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(patient_id__icontains=query) |
            Q(phone__icontains=query)
        )
    if reg_type:
        patients = patients.filter(registration_type=reg_type)
    return render(request, 'patients/patient_list.html', {
        'patients': patients, 'query': query, 'reg_type': reg_type,
    })


@login_required
def patient_add(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient registered successfully!')
            return redirect('patients:patient_list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Register New Patient'})


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    appointments = patient.appointments.select_related('doctor').all()[:10]
    return render(request, 'patients/patient_detail.html', {
        'patient': patient, 'appointments': appointments,
    })


@login_required
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('patients:patient_detail', pk=pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form, 'title': 'Edit Patient'})


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.is_active = False
        patient.save()
        messages.success(request, 'Patient record deactivated.')
        return redirect('patients:patient_list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})
