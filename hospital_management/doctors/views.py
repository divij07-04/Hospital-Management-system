from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Doctor
from .forms import DoctorForm


@login_required
def doctor_list(request):
    query = request.GET.get('q', '')
    spec = request.GET.get('specialization', '')
    doctors = Doctor.objects.select_related('user').all()
    if query:
        doctors = doctors.filter(
            user__first_name__icontains=query
        ) | doctors.filter(
            user__last_name__icontains=query
        ) | doctors.filter(
            doctor_id__icontains=query
        )
    if spec:
        doctors = doctors.filter(specialization=spec)
    specializations = Doctor.SPECIALIZATION_CHOICES
    return render(request, 'doctors/doctor_list.html', {
        'doctors': doctors, 'query': query, 'spec': spec,
        'specializations': specializations,
    })


@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor.objects.select_related('user'), pk=pk)
    appointments = doctor.appointments.select_related('patient').all()[:10]
    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor, 'appointments': appointments,
    })


@login_required
def doctor_edit(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user.first_name = form.cleaned_data['first_name']
            doctor.user.last_name = form.cleaned_data['last_name']
            doctor.user.email = form.cleaned_data['email']
            doctor.user.phone = form.cleaned_data['phone']
            doctor.user.save()
            doctor.save()
            messages.success(request, 'Doctor profile updated!')
            return redirect('doctors:doctor_detail', pk=pk)
    else:
        form = DoctorForm(instance=doctor, initial={
            'first_name': doctor.user.first_name,
            'last_name': doctor.user.last_name,
            'email': doctor.user.email,
            'phone': doctor.user.phone,
        })
    return render(request, 'doctors/doctor_form.html', {'form': form, 'title': 'Edit Doctor'})
