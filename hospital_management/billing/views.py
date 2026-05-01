from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Invoice, InvoiceItem
from .forms import InvoiceForm, InvoiceItemFormSet, PaymentForm
from appointments.models import Appointment


@login_required
def invoice_list(request):
    status_filter = request.GET.get('status', '')
    invoices = Invoice.objects.select_related('appointment', 'appointment__patient').all()
    if status_filter:
        invoices = invoices.filter(status=status_filter)
    return render(request, 'billing/invoice_list.html', {
        'invoices': invoices, 'status_filter': status_filter,
    })


@login_required
def invoice_create(request, appointment_pk):
    appointment = get_object_or_404(Appointment, pk=appointment_pk)
    if hasattr(appointment, 'invoice'):
        messages.info(request, 'Invoice already exists for this appointment.')
        return redirect('billing:invoice_detail', pk=appointment.invoice.pk)

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            invoice = form.save(commit=False)
            invoice.appointment = appointment
            invoice.save()
            formset.instance = invoice
            formset.save()
            # Calculate total
            total = sum(item.line_total for item in invoice.items.all())
            total += appointment.doctor.consultation_fee
            invoice.total_amount = total
            invoice.save()
            messages.success(request, 'Invoice generated!')
            return redirect('billing:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(initial={'appointment': appointment})
        formset = InvoiceItemFormSet()
    return render(request, 'billing/invoice_form.html', {
        'form': form, 'formset': formset, 'appointment': appointment,
    })


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(
        Invoice.objects.select_related(
            'appointment', 'appointment__patient', 'appointment__doctor', 'appointment__doctor__user'
        ), pk=pk
    )
    items = invoice.items.all()
    return render(request, 'billing/invoice_detail.html', {
        'invoice': invoice, 'items': items,
    })


@login_required
def invoice_pay(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            invoice.paid_amount += amount
            if invoice.paid_amount >= invoice.net_amount:
                invoice.status = 'paid'
            else:
                invoice.status = 'partial'
            invoice.save()
            messages.success(request, f'Payment of ₹{amount} recorded!')
            return redirect('billing:invoice_detail', pk=pk)
    else:
        form = PaymentForm(initial={'amount': invoice.due_amount})
    return render(request, 'billing/invoice_pay.html', {
        'form': form, 'invoice': invoice,
    })
