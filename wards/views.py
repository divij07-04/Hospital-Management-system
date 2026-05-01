from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Ward, Bed
from .forms import WardForm, BedForm
from patients.models import Patient


@login_required
def ward_list(request):
    wards = Ward.objects.prefetch_related('beds').all()
    return render(request, 'wards/ward_list.html', {'wards': wards})


@login_required
def ward_add(request):
    if request.method == 'POST':
        form = WardForm(request.POST)
        if form.is_valid():
            ward = form.save()
            # Auto-create beds based on capacity
            for i in range(1, ward.capacity + 1):
                Bed.objects.create(ward=ward, bed_number=f'{i:02d}')
            messages.success(request, f'Ward "{ward.name}" created with {ward.capacity} beds!')
            return redirect('wards:ward_list')
    else:
        form = WardForm()
    return render(request, 'wards/ward_form.html', {'form': form, 'title': 'Add Ward'})


@login_required
def ward_detail(request, pk):
    ward = get_object_or_404(Ward.objects.prefetch_related('beds', 'beds__patient'), pk=pk)
    beds = ward.beds.all()
    available_patients = Patient.objects.filter(
        is_active=True, registration_type='IPD'
    ).exclude(
        bed__status='occupied'
    )
    return render(request, 'wards/ward_detail.html', {
        'ward': ward, 'beds': beds, 'available_patients': available_patients,
    })


@login_required
def bed_admit(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        if patient_id:
            patient = get_object_or_404(Patient, pk=patient_id)
            bed.patient = patient
            bed.status = 'occupied'
            bed.admitted_on = timezone.now()
            bed.save()
            messages.success(request, f'{patient.full_name} admitted to {bed}.')
        return redirect('wards:ward_detail', pk=bed.ward.pk)
    return redirect('wards:ward_detail', pk=bed.ward.pk)


@login_required
def bed_discharge(request, pk):
    bed = get_object_or_404(Bed, pk=pk)
    if request.method == 'POST':
        patient_name = bed.patient.full_name if bed.patient else 'Patient'
        bed.patient = None
        bed.status = 'available'
        bed.admitted_on = None
        bed.save()
        messages.success(request, f'{patient_name} discharged from {bed}.')
    return redirect('wards:ward_detail', pk=bed.ward.pk)
