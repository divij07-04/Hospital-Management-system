"""
Seed CURA with demo data for lab demonstrations.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from core.models import User
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment
from pharmacy.models import Medicine, Prescription, PrescriptionItem
from billing.models import Invoice, InvoiceItem
from wards.models import Ward, Bed


class Command(BaseCommand):
    help = 'Seeds the CURA database with realistic demo data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('🌱 Seeding CURA database...'))

        # ---- Admin User ----
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@cura.health',
                'first_name': 'Arjun',
                'last_name': 'Mehta',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone': '9876543210',
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Admin user created (admin / admin123)'))

        # ---- Receptionist ----
        recep, created = User.objects.get_or_create(
            username='receptionist',
            defaults={
                'email': 'reception@cura.health',
                'first_name': 'Priya',
                'last_name': 'Sharma',
                'role': 'receptionist',
                'phone': '9876543211',
            }
        )
        if created:
            recep.set_password('recep123')
            recep.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Receptionist user created (receptionist / recep123)'))

        # ---- Doctors ----
        doctors_data = [
            {'username': 'dr.ananya', 'first_name': 'Ananya', 'last_name': 'Reddy', 'email': 'ananya@cura.health',
             'spec': 'cardiology', 'qual': 'MBBS, MD (Cardiology)', 'exp': 12, 'fee': 800,
             'days': 'mon,tue,wed,thu,fri', 'bio': 'Passionate about preventive cardiology and heart health awareness.'},
            {'username': 'dr.rahul', 'first_name': 'Rahul', 'last_name': 'Kapoor', 'email': 'rahul@cura.health',
             'spec': 'orthopedics', 'qual': 'MBBS, MS (Ortho)', 'exp': 8, 'fee': 700,
             'days': 'mon,wed,fri,sat', 'bio': 'Specializes in sports injuries and joint replacement surgery.'},
            {'username': 'dr.meera', 'first_name': 'Meera', 'last_name': 'Nair', 'email': 'meera@cura.health',
             'spec': 'pediatrics', 'qual': 'MBBS, MD (Pediatrics)', 'exp': 15, 'fee': 600,
             'days': 'mon,tue,thu,fri,sat', 'bio': 'Every child deserves gentle, attentive care.'},
            {'username': 'dr.vikram', 'first_name': 'Vikram', 'last_name': 'Singh', 'email': 'vikram@cura.health',
             'spec': 'neurology', 'qual': 'MBBS, DM (Neurology)', 'exp': 10, 'fee': 900,
             'days': 'tue,wed,thu,fri', 'bio': 'Dedicated to understanding the complexities of the human brain.'},
            {'username': 'dr.sana', 'first_name': 'Sana', 'last_name': 'Farooqui', 'email': 'sana@cura.health',
             'spec': 'dermatology', 'qual': 'MBBS, MD (Dermatology)', 'exp': 6, 'fee': 650,
             'days': 'mon,tue,wed,sat', 'bio': 'Helping people feel confident in their own skin.'},
        ]
        doctor_objs = []
        for d in doctors_data:
            user, created = User.objects.get_or_create(
                username=d['username'],
                defaults={
                    'email': d['email'],
                    'first_name': d['first_name'],
                    'last_name': d['last_name'],
                    'role': 'doctor',
                    'phone': f'98765{len(doctor_objs)+43212}',
                }
            )
            if created:
                user.set_password('doctor123')
                user.save()

            doc, _ = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    'specialization': d['spec'],
                    'qualification': d['qual'],
                    'experience_years': d['exp'],
                    'consultation_fee': Decimal(str(d['fee'])),
                    'available_days': d['days'],
                    'bio': d['bio'],
                }
            )
            doctor_objs.append(doc)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(doctor_objs)} doctors ready'))

        # ---- Patients ----
        patients_data = [
            {'fn': 'Aditya', 'ln': 'Kumar', 'dob': date(1990, 5, 15), 'g': 'M', 'bg': 'O+', 'ph': '9100000001', 'reg': 'OPD',
             'allergies': 'Penicillin', 'chronic': 'Mild asthma'},
            {'fn': 'Sneha', 'ln': 'Patel', 'dob': date(1985, 8, 22), 'g': 'F', 'bg': 'A+', 'ph': '9100000002', 'reg': 'OPD',
             'allergies': '', 'chronic': 'Hypertension'},
            {'fn': 'Rohan', 'ln': 'Das', 'dob': date(2015, 3, 10), 'g': 'M', 'bg': 'B+', 'ph': '9100000003', 'reg': 'OPD',
             'allergies': 'Dust', 'chronic': ''},
            {'fn': 'Kavya', 'ln': 'Iyer', 'dob': date(1978, 11, 30), 'g': 'F', 'bg': 'AB-', 'ph': '9100000004', 'reg': 'IPD',
             'allergies': '', 'chronic': 'Diabetes Type 2'},
            {'fn': 'Imran', 'ln': 'Khan', 'dob': date(1995, 1, 8), 'g': 'M', 'bg': 'O-', 'ph': '9100000005', 'reg': 'OPD',
             'allergies': 'Sulfa drugs', 'chronic': ''},
            {'fn': 'Lakshmi', 'ln': 'Menon', 'dob': date(2000, 7, 4), 'g': 'F', 'bg': 'A-', 'ph': '9100000006', 'reg': 'IPD',
             'allergies': '', 'chronic': ''},
            {'fn': 'Arjun', 'ln': 'Rao', 'dob': date(1960, 12, 20), 'g': 'M', 'bg': 'B-', 'ph': '9100000007', 'reg': 'IPD',
             'allergies': 'NSAIDS', 'chronic': 'Heart disease, Diabetes'},
            {'fn': 'Diya', 'ln': 'Bose', 'dob': date(2018, 6, 1), 'g': 'F', 'bg': 'O+', 'ph': '9100000008', 'reg': 'OPD',
             'allergies': '', 'chronic': ''},
        ]
        patient_objs = []
        for p in patients_data:
            patient, _ = Patient.objects.get_or_create(
                phone=p['ph'],
                defaults={
                    'first_name': p['fn'], 'last_name': p['ln'],
                    'date_of_birth': p['dob'], 'gender': p['g'],
                    'blood_group': p['bg'], 'registration_type': p['reg'],
                    'allergies': p['allergies'], 'chronic_conditions': p['chronic'],
                    'emergency_contact_name': 'Family Member',
                    'emergency_contact_phone': f'91000099{len(patient_objs)+1:02d}',
                }
            )
            patient_objs.append(patient)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(patient_objs)} patients registered'))

        # ---- Medicines ----
        medicines_data = [
            {'name': 'Paracetamol 500mg', 'generic': 'Acetaminophen', 'cat': 'tablet', 'price': 12, 'qty': 500, 'mfr': 'Cipla'},
            {'name': 'Amoxicillin 250mg', 'generic': 'Amoxicillin', 'cat': 'capsule', 'price': 25, 'qty': 200, 'mfr': 'Sun Pharma'},
            {'name': 'Cough Syrup', 'generic': 'Dextromethorphan', 'cat': 'syrup', 'price': 85, 'qty': 80, 'mfr': 'Dabur'},
            {'name': 'Omeprazole 20mg', 'generic': 'Omeprazole', 'cat': 'capsule', 'price': 18, 'qty': 300, 'mfr': 'Dr. Reddy\'s'},
            {'name': 'Cetirizine 10mg', 'generic': 'Cetirizine', 'cat': 'tablet', 'price': 8, 'qty': 8, 'mfr': 'Mankind', 'low': True},
            {'name': 'Metformin 500mg', 'generic': 'Metformin', 'cat': 'tablet', 'price': 15, 'qty': 400, 'mfr': 'USV'},
            {'name': 'Betadine Ointment', 'generic': 'Povidone-Iodine', 'cat': 'ointment', 'price': 65, 'qty': 50, 'mfr': 'Win-Medicare'},
            {'name': 'Insulin Injection', 'generic': 'Insulin Glargine', 'cat': 'injection', 'price': 450, 'qty': 5, 'mfr': 'Novo Nordisk', 'low': True},
            {'name': 'Eye Drops (Moxifloxacin)', 'generic': 'Moxifloxacin', 'cat': 'drops', 'price': 120, 'qty': 40, 'mfr': 'Alcon'},
            {'name': 'Salbutamol Inhaler', 'generic': 'Albuterol', 'cat': 'inhaler', 'price': 180, 'qty': 25, 'mfr': 'Cipla'},
        ]
        med_objs = []
        for m in medicines_data:
            med, _ = Medicine.objects.get_or_create(
                name=m['name'],
                defaults={
                    'generic_name': m['generic'],
                    'category': m['cat'],
                    'price': Decimal(str(m['price'])),
                    'quantity_in_stock': m['qty'],
                    'manufacturer': m['mfr'],
                    'reorder_level': 10,
                    'expiry_date': date.today() + timedelta(days=365),
                }
            )
            med_objs.append(med)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(med_objs)} medicines stocked'))

        # ---- Appointments ----
        today = date.today()
        appointments_data = [
            {'patient': 0, 'doctor': 0, 'date': today, 'time': '10:00', 'status': 'completed', 'reason': 'Routine heart checkup'},
            {'patient': 1, 'doctor': 0, 'date': today, 'time': '11:00', 'status': 'confirmed', 'reason': 'Blood pressure follow-up'},
            {'patient': 2, 'doctor': 2, 'date': today, 'time': '09:30', 'status': 'completed', 'reason': 'Fever and cold'},
            {'patient': 3, 'doctor': 3, 'date': today - timedelta(days=1), 'time': '14:00', 'status': 'completed', 'reason': 'Migraine evaluation'},
            {'patient': 4, 'doctor': 4, 'date': today + timedelta(days=1), 'time': '10:30', 'status': 'pending', 'reason': 'Skin rash'},
            {'patient': 5, 'doctor': 1, 'date': today + timedelta(days=1), 'time': '11:30', 'status': 'pending', 'reason': 'Knee pain'},
            {'patient': 6, 'doctor': 0, 'date': today - timedelta(days=2), 'time': '15:00', 'status': 'completed', 'reason': 'Chest pain investigation'},
            {'patient': 7, 'doctor': 2, 'date': today + timedelta(days=2), 'time': '09:00', 'status': 'pending', 'reason': 'Vaccination'},
        ]
        apt_objs = []
        for a in appointments_data:
            apt, created = Appointment.objects.get_or_create(
                doctor=doctor_objs[a['doctor']],
                date=a['date'],
                time_slot=a['time'],
                defaults={
                    'patient': patient_objs[a['patient']],
                    'status': a['status'],
                    'reason': a['reason'],
                    'diagnosis': 'Initial assessment completed' if a['status'] == 'completed' else '',
                }
            )
            apt_objs.append(apt)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(apt_objs)} appointments created'))

        # ---- Prescriptions for completed appointments ----
        for apt in apt_objs:
            if apt.status == 'completed' and not hasattr(apt, 'prescription'):
                presc = Prescription.objects.create(
                    appointment=apt,
                    notes='Take medicines as prescribed. Follow up after 7 days.'
                )
                # Add 2 random medicines
                PrescriptionItem.objects.create(
                    prescription=presc, medicine=med_objs[0],
                    dosage='1-0-1', duration_days=5, quantity=10, instructions='After food'
                )
                PrescriptionItem.objects.create(
                    prescription=presc, medicine=med_objs[3],
                    dosage='1-0-0', duration_days=7, quantity=7, instructions='Before breakfast'
                )
        self.stdout.write(self.style.SUCCESS('  ✓ Prescriptions written'))

        # ---- Invoices for completed appointments ----
        for apt in apt_objs:
            if apt.status == 'completed' and not hasattr(apt, 'invoice'):
                inv = Invoice.objects.create(
                    appointment=apt,
                    total_amount=apt.doctor.consultation_fee + Decimal('200'),
                    discount=Decimal('0'),
                    paid_amount=apt.doctor.consultation_fee + Decimal('200'),
                    status='paid',
                )
                InvoiceItem.objects.create(
                    invoice=inv, description=f'Consultation — Dr. {apt.doctor.user.get_full_name()}',
                    quantity=1, unit_price=apt.doctor.consultation_fee
                )
                InvoiceItem.objects.create(
                    invoice=inv, description='Lab Test — Blood Panel',
                    quantity=1, unit_price=Decimal('200')
                )
        self.stdout.write(self.style.SUCCESS('  ✓ Invoices generated'))

        # ---- Wards & Beds ----
        wards_data = [
            {'name': 'General Ward A', 'type': 'general', 'floor': 1, 'cap': 12, 'charge': 500},
            {'name': 'General Ward B', 'type': 'general', 'floor': 1, 'cap': 10, 'charge': 500},
            {'name': 'Private Wing', 'type': 'private', 'floor': 2, 'cap': 6, 'charge': 2500},
            {'name': 'ICU', 'type': 'icu', 'floor': 3, 'cap': 8, 'charge': 5000},
            {'name': 'Pediatric Ward', 'type': 'semi_private', 'floor': 2, 'cap': 8, 'charge': 1500},
        ]
        for w in wards_data:
            ward, created = Ward.objects.get_or_create(
                name=w['name'],
                defaults={
                    'ward_type': w['type'],
                    'floor': w['floor'],
                    'capacity': w['cap'],
                    'charge_per_day': Decimal(str(w['charge'])),
                }
            )
            if created:
                for i in range(1, w['cap'] + 1):
                    Bed.objects.create(ward=ward, bed_number=f'{i:02d}')

        # Admit IPD patients
        ipd_patients = Patient.objects.filter(registration_type='IPD', is_active=True)
        available_beds = list(Bed.objects.filter(status='available')[:3])
        for i, patient in enumerate(ipd_patients[:len(available_beds)]):
            bed = available_beds[i]
            bed.patient = patient
            bed.status = 'occupied'
            bed.admitted_on = timezone.now() - timedelta(days=i + 1)
            bed.save()

        # Mark a couple as reserved / maintenance
        Bed.objects.filter(status='available').order_by('?').first()
        maint_beds = Bed.objects.filter(status='available').order_by('?')[:2]
        for b in maint_beds:
            b.status = 'maintenance'
            b.save()

        self.stdout.write(self.style.SUCCESS('  ✓ Wards & beds configured'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 CURA is ready! Demo credentials:'))
        self.stdout.write(self.style.WARNING('   Admin:        admin / admin123'))
        self.stdout.write(self.style.WARNING('   Receptionist: receptionist / recep123'))
        self.stdout.write(self.style.WARNING('   Doctors:      dr.ananya / doctor123  (and others)'))
        self.stdout.write('')
        self.stdout.write(self.style.MIGRATE_HEADING('   Run: python manage.py runserver'))
