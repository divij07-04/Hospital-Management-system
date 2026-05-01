from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medicine, Prescription, PrescriptionItem
from .forms import MedicineForm, PrescriptionForm, PrescriptionItemFormSet
from appointments.models import Appointment


@login_required
def medicine_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    medicines = Medicine.objects.all()
    if query:
        medicines = medicines.filter(name__icontains=query)
    if category:
        medicines = medicines.filter(category=category)
    low_stock = Medicine.objects.filter(
        quantity_in_stock__lte=models.F('reorder_level')
    )
    return render(request, 'pharmacy/medicine_list.html', {
        'medicines': medicines, 'query': query, 'category': category,
        'low_stock': low_stock,
        'categories': Medicine.CATEGORY_CHOICES,
    })


@login_required
def medicine_add(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine added to inventory!')
            return redirect('pharmacy:medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'pharmacy/medicine_form.html', {'form': form, 'title': 'Add Medicine'})


@login_required
def medicine_edit(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine updated!')
            return redirect('pharmacy:medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'pharmacy/medicine_form.html', {'form': form, 'title': 'Edit Medicine'})


@login_required
def prescription_create(request, appointment_pk):
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    if hasattr(appointment, 'prescription'):
        messages.info(request, 'Prescription already exists for this appointment.')
        return redirect('pharmacy:prescription_detail', pk=appointment.prescription.pk)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        formset = PrescriptionItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.save()
            formset.instance = prescription
            formset.save()
            messages.success(request, 'Prescription created!')
            return redirect('pharmacy:prescription_detail', pk=prescription.pk)
    else:
        form = PrescriptionForm()
        formset = PrescriptionItemFormSet()
    return render(request, 'pharmacy/prescription_form.html', {
        'form': form, 'formset': formset, 'appointment': appointment,
    })


@login_required
def prescription_detail(request, pk):
    prescription = get_object_or_404(
        Prescription.objects.select_related('appointment', 'appointment__patient', 'appointment__doctor'), pk=pk
    )
    items = prescription.items.select_related('medicine').all()
    return render(request, 'pharmacy/prescription_detail.html', {
        'prescription': prescription, 'items': items,
    })


# Need models import for F expression
from django.db import models
