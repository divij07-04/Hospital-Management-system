[README.md](https://github.com/user-attachments/files/27279732/README.md)
# 🏥 CURA — Hospital Management System

### *Care You Rely on, Always*

> A comprehensive, Django-based Hospital Management System designed with a **patient-first philosophy**. CURA digitises the entire hospital workflow — from patient registration and doctor appointments to prescriptions, billing, and ward/bed management — all wrapped in a warm, humanised, and visually stunning interface.

---

## 📋 Table of Contents

1. [Abstract](#-abstract)
2. [Introduction](#-introduction)
3. [Objectives](#-objectives)
4. [Technology Stack](#-technology-stack)
5. [System Architecture](#-system-architecture)
6. [Project Structure](#-project-structure)
7. [Database Design — Models & ER Diagram](#-database-design--models--er-diagram)
8. [Module-wise Description](#-module-wise-description)
   - [Core Module](#1-core-module--authentication--dashboard)
   - [Patients Module](#2-patients-module)
   - [Doctors Module](#3-doctors-module)
   - [Appointments Module](#4-appointments-module)
   - [Pharmacy Module](#5-pharmacy-module)
   - [Billing Module](#6-billing-module)
   - [Wards & Beds Module](#7-wards--beds-module)
9. [URL Routing](#-url-routing)
10. [Template System](#-template-system)
11. [UI/UX Design Philosophy](#-uiux-design-philosophy)
12. [Unique Features](#-unique-features-what-makes-cura-different)
13. [OPD Workflow — Patient Journey](#-opd-workflow--the-patient-journey)
14. [Screenshots](#-screenshots)
15. [Installation & Setup](#-installation--setup)
16. [Demo Credentials](#-demo-credentials)
17. [Future Enhancements](#-future-enhancements)
18. [Conclusion](#-conclusion)

---

## 📝 Abstract

**CURA** is a full-featured Hospital Management System built using the **Django web framework** (Python) and **Bootstrap 5** for the frontend. The system addresses the core operational needs of a hospital by providing dedicated modules for managing patients, doctors, appointments, pharmacy/prescriptions, billing/invoices, and ward/bed occupancy — all accessible through a role-based dashboard with real-time analytics.

What sets CURA apart from typical HMS implementations is its **humanised design approach**: every screen uses warm, empathetic language; the interface features a soothing light-pink, white, and red color palette; and the system includes unique features like a visual **OPD Workflow Tracker**, a color-coded **Bed Occupancy Map**, **auto-generated unique IDs** (e.g., `CURA-P00001`), and **print-friendly prescriptions and invoices** with branded headers.

The project follows Django best practices including a custom user model, app-based modular architecture, template inheritance, model-form separation, and management commands for data seeding.

---

## 🏁 Introduction

Hospitals handle an enormous volume of data daily — patient records, doctor schedules, appointment bookings, medicine inventories, billing transactions, and bed allocation. Managing all of this on paper or in disconnected spreadsheets leads to errors, delays, and a frustrating experience for both staff and patients.

**CURA** solves this by providing a **single, unified web interface** where:
- **Receptionists** can register patients and book appointments in seconds.
- **Doctors** can view their appointment schedules, write digital prescriptions, and add diagnoses.
- **Administrators** can monitor hospital-wide metrics through a dashboard, manage pharmacy stock, generate invoices, and oversee ward occupancy.

The name **CURA** comes from the Latin word for "care" — reflecting the system's core belief that technology should serve people, not overwhelm them.

---

## 🎯 Objectives

1. **Digitise hospital operations** — Replace paper-based processes with a secure, searchable, digital system.
2. **Streamline patient flow** — Provide an end-to-end OPD/IPD workflow: Registration → Appointment → Diagnosis → Prescription → Billing → Discharge.
3. **Enable real-time monitoring** — Dashboard with stat cards and Chart.js analytics for appointments, revenue, bed occupancy, and pharmacy alerts.
4. **Support role-based access** — Different views for Admin, Doctor, Patient, and Receptionist roles.
5. **Ensure data integrity** — Auto-generated unique IDs, form validation, and relational database constraints.
6. **Provide a humane, accessible UI** — Warm color palette, friendly copy, responsive design, and print-friendly documents.

---

## 💻 Technology Stack

| Layer | Technology | Version | Purpose |
|---|---|---|---|
| **Backend Framework** | Django | 4.2 LTS | Web framework, ORM, URL routing, templating |
| **Language** | Python | 3.11 | Server-side logic |
| **Database** | SQLite3 | Built-in | Lightweight relational database (zero setup) |
| **Frontend Framework** | Bootstrap | 5.3.2 | Responsive grid, components, utilities |
| **Icons** | Bootstrap Icons | 1.11.3 | Icon library for UI elements |
| **Typography** | Google Fonts (Poppins) | — | Modern, clean typeface |
| **Charts** | Chart.js | 4.4.1 | Dashboard analytics (bar, doughnut charts) |
| **Custom CSS** | Vanilla CSS | — | CURA theme (light pink / white / red palette) |

### Why These Choices?

- **Django** was chosen for its "batteries-included" philosophy — built-in admin panel, ORM, form handling, authentication, and template engine reduce boilerplate.
- **SQLite3** requires zero configuration, making the project portable and ideal for lab demos.
- **Bootstrap 5** provides responsive, accessible components out of the box, overlaid with our custom CURA theme CSS.
- **Chart.js** enables interactive, animated charts without heavy dependencies.

---

## 🏗 System Architecture

CURA follows the **MVT (Model–View–Template)** architecture pattern native to Django:

```
┌──────────────────────────────────────────────────────────┐
│                      BROWSER (Client)                     │
│   Bootstrap 5 + CURA CSS + Chart.js + Bootstrap Icons     │
└──────────────────────┬───────────────────────────────────┘
                       │ HTTP Request
                       ▼
┌──────────────────────────────────────────────────────────┐
│                    URL DISPATCHER                          │
│         hospital_management/urls.py → App URLs             │
└──────────────────────┬───────────────────────────────────┘
                       │ Route Match
                       ▼
┌──────────────────────────────────────────────────────────┐
│                      VIEWS (Logic)                        │
│   core/views.py, patients/views.py, doctors/views.py ...  │
│   - Query models, process forms, build context             │
└──────────────┬───────────────────┬───────────────────────┘
               │ ORM Queries       │ Context Dict
               ▼                   ▼
┌──────────────────────┐  ┌────────────────────────────────┐
│    MODELS (Database)  │  │     TEMPLATES (Presentation)    │
│  core/models.py       │  │  templates/base.html            │
│  patients/models.py   │  │  templates/core/dashboard.html  │
│  doctors/models.py    │  │  templates/patients/...         │
│  appointments/...     │  │  ...                            │
│  pharmacy/...         │  │  Inherits base.html             │
│  billing/...          │  │  Uses Bootstrap + CURA CSS      │
│  wards/...            │  └────────────────────────────────┘
│                       │
│  SQLite3 Database     │
└──────────────────────┘
```

### Request-Response Flow

1. User sends an HTTP request (e.g., `GET /patients/`).
2. Django's URL dispatcher matches the path to `patients/urls.py → patient_list` view.
3. The view function queries the `Patient` model via Django ORM.
4. Results are passed as context to `patients/patient_list.html`.
5. The template extends `base.html` (which provides the sidebar, topbar, and footer).
6. The rendered HTML is returned as an HTTP response.

---

## 📂 Project Structure

```
c:\_Work_\WPL\
│
├── manage.py                          # Django management utility
├── requirements.txt                   # Project dependencies
├── db.sqlite3                         # SQLite database (auto-created)
│
├── hospital_management/               # Project configuration
│   ├── __init__.py
│   ├── settings.py                    # Settings (apps, DB, static, auth model)
│   ├── urls.py                        # Root URL configuration
│   └── wsgi.py                        # WSGI application entry point
│
├── core/                              # Core app — Auth, Dashboard, User model
│   ├── models.py                      # Custom User model, Notification model
│   ├── views.py                       # Login, logout, dashboard, profile views
│   ├── forms.py                       # Login form, profile edit form
│   ├── urls.py                        # URL patterns for core routes
│   ├── admin.py                       # Admin registrations
│   └── management/commands/
│       └── seed_data.py               # Management command to seed demo data
│
├── patients/                          # Patients app
│   ├── models.py                      # Patient model (with auto-ID generation)
│   ├── views.py                       # List, add, detail, edit, delete views
│   ├── forms.py                       # PatientForm (ModelForm)
│   ├── urls.py                        # URL patterns (CRUD)
│   └── admin.py                       # Admin registration with search/filter
│
├── doctors/                           # Doctors app
│   ├── models.py                      # Doctor model (linked to User)
│   ├── views.py                       # List, detail, edit views
│   ├── forms.py                       # DoctorForm (with user fields)
│   ├── urls.py                        # URL patterns
│   └── admin.py                       # Admin registration
│
├── appointments/                      # Appointments app
│   ├── models.py                      # Appointment model (with time slots)
│   ├── views.py                       # List, add, detail, update, cancel views
│   ├── forms.py                       # AppointmentForm, AppointmentStatusForm
│   ├── urls.py                        # URL patterns
│   └── admin.py                       # Admin registration
│
├── pharmacy/                          # Pharmacy app
│   ├── models.py                      # Medicine, Prescription, PrescriptionItem
│   ├── views.py                       # Medicine CRUD, prescription create/detail
│   ├── forms.py                       # MedicineForm, PrescriptionItemFormSet
│   ├── urls.py                        # URL patterns
│   └── admin.py                       # Admin with inline prescription items
│
├── billing/                           # Billing app
│   ├── models.py                      # Invoice, InvoiceItem models
│   ├── views.py                       # Invoice list, create, detail, payment
│   ├── forms.py                       # InvoiceForm, InvoiceItemFormSet, PaymentForm
│   ├── urls.py                        # URL patterns
│   └── admin.py                       # Admin with inline invoice items
│
├── wards/                             # Wards & Beds app
│   ├── models.py                      # Ward, Bed models
│   ├── views.py                       # Ward list/add/detail, bed admit/discharge
│   ├── forms.py                       # WardForm, BedForm
│   ├── urls.py                        # URL patterns
│   └── admin.py                       # Admin with inline beds
│
├── templates/                         # All HTML templates
│   ├── base.html                      # Master layout (sidebar + topbar + messages)
│   ├── core/
│   │   ├── home.html                  # Landing page
│   │   ├── login.html                 # Login page
│   │   ├── dashboard.html             # Dashboard with charts & stats
│   │   └── profile.html              # User profile edit
│   ├── patients/
│   │   ├── patient_list.html          # Patient table with search/filter
│   │   ├── patient_form.html          # Add/Edit patient form
│   │   ├── patient_detail.html        # Patient profile + history
│   │   └── patient_confirm_delete.html # Soft-delete confirmation
│   ├── doctors/
│   │   ├── doctor_list.html           # Doctor card grid
│   │   ├── doctor_detail.html         # Doctor profile + appointments
│   │   └── doctor_form.html           # Edit doctor form
│   ├── appointments/
│   │   ├── appointment_list.html      # Appointment table + status filters
│   │   ├── appointment_form.html      # Book appointment
│   │   ├── appointment_detail.html    # Detail + workflow tracker + actions
│   │   ├── appointment_update.html    # Update status/diagnosis
│   │   └── appointment_confirm_cancel.html  # Cancel confirmation
│   ├── pharmacy/
│   │   ├── medicine_list.html         # Medicine inventory table
│   │   ├── medicine_form.html         # Add/Edit medicine
│   │   ├── prescription_form.html     # Write prescription (inline formset)
│   │   └── prescription_detail.html   # Print-ready prescription
│   ├── billing/
│   │   ├── invoice_list.html          # Invoice table + status filter
│   │   ├── invoice_form.html          # Generate invoice (inline items)
│   │   ├── invoice_detail.html        # Print-ready invoice
│   │   └── invoice_pay.html           # Record payment
│   └── wards/
│       ├── ward_list.html             # Ward cards + bed occupancy grid
│       ├── ward_form.html             # Add ward
│       └── ward_detail.html           # Bed management table (admit/discharge)
│
└── static/
    └── css/
        └── cura.css                   # Complete CURA theme stylesheet
```

---

## 🗄 Database Design — Models & ER Diagram

### Entity-Relationship Diagram

```
┌─────────────┐       ┌──────────────┐       ┌─────────────────┐
│    User      │       │   Doctor     │       │    Patient      │
│ (Custom)     │       │              │       │                 │
│──────────────│       │──────────────│       │─────────────────│
│ id (PK)      │◄──┐  │ id (PK)      │       │ id (PK)         │
│ username     │   │  │ user (FK→User)│       │ user (FK→User)  │
│ email        │   │  │ specialization│       │ first_name      │
│ first_name   │   │  │ qualification │       │ last_name       │
│ last_name    │   │  │ experience    │       │ date_of_birth   │
│ role         │   │  │ cons_fee      │       │ gender          │
│ phone        │   │  │ available_days│       │ blood_group     │
│ profile_pic  │   │  │ doctor_id     │       │ phone           │
│ address      │   │  │ bio           │       │ registration    │
│ is_staff     │   │  └───────┬───────┘       │ allergies       │
│ is_superuser │   │          │               │ chronic_cond    │
└──────────────┘   │          │               │ patient_id      │
                   │          │               └────────┬────────┘
                   │          │                        │
                   │     ┌────┴────────────────────────┴───┐
                   │     │          Appointment              │
                   │     │──────────────────────────────────│
                   │     │ id (PK)                          │
                   │     │ patient (FK→Patient)              │
                   │     │ doctor (FK→Doctor)                │
                   │     │ date                              │
                   │     │ time_slot                         │
                   │     │ status                            │
                   │     │ reason, diagnosis, notes          │
                   │     │ appointment_id (auto)             │
                   │     └────────┬───────────┬─────────────┘
                   │              │           │
               ┌───┴──────────┐   │    ┌──────┴──────────┐
               │ Notification │   │    │   Prescription   │
               │──────────────│   │    │─────────────────│
               │ user (FK)    │   │    │ appointment (1:1)│
               │ title        │   │    │ notes            │
               │ message      │   │    └────────┬────────┘
               │ is_read      │   │             │
               └──────────────┘   │    ┌────────┴─────────┐
                                  │    │PrescriptionItem   │
                                  │    │──────────────────│
                                  │    │ prescription (FK) │
                                  │    │ medicine (FK)     │
                                  │    │ dosage            │
                                  │    │ duration_days     │
                                  │    │ quantity          │
                                  │    │ instructions      │
                                  │    └────────┬─────────┘
                                  │             │
                                  │    ┌────────┴────┐
                                  │    │  Medicine    │
                                  │    │─────────────│
                                  │    │ name         │
                                  │    │ generic_name │
                                  │    │ category     │
                                  │    │ price        │
                                  │    │ qty_in_stock │
                                  │    │ reorder_level│
                                  │    │ expiry_date  │
                                  │    └─────────────┘
                                  │
                           ┌──────┴──────────┐
                           │    Invoice       │
                           │─────────────────│
                           │ appointment (1:1)│
                           │ invoice_id (auto)│
                           │ total_amount     │
                           │ discount         │
                           │ paid_amount      │
                           │ status           │
                           └────────┬────────┘
                                    │
                           ┌────────┴────────┐
                           │  InvoiceItem    │
                           │─────────────────│
                           │ invoice (FK)    │
                           │ description     │
                           │ quantity        │
                           │ unit_price      │
                           └─────────────────┘

┌────────────┐       ┌───────────────┐
│   Ward     │       │     Bed       │
│────────────│       │───────────────│
│ id (PK)    │◄──────│ ward (FK)     │
│ name       │       │ bed_number    │
│ ward_type  │       │ status        │
│ floor      │       │ patient (FK)  │
│ capacity   │       │ admitted_on   │
│ charge/day │       │ notes         │
└────────────┘       └───────────────┘
```

### Detailed Model Descriptions

#### 1. **User** (`core/models.py`)
Extends Django's `AbstractUser` to add hospital-specific fields.

| Field | Type | Description |
|---|---|---|
| `role` | CharField (choices) | One of: `admin`, `doctor`, `patient`, `receptionist` |
| `phone` | CharField(15) | Contact phone number |
| `profile_pic` | URLField | Profile picture URL |
| `address` | TextField | Residential address |

**Properties:** `is_admin_user`, `is_doctor`, `is_patient`, `is_receptionist`

---

#### 2. **Patient** (`patients/models.py`)
Stores comprehensive patient information with auto-generated CURA IDs.

| Field | Type | Description |
|---|---|---|
| `patient_id` | CharField (auto) | Format: `CURA-P00001` (auto-generated, unique) |
| `first_name` / `last_name` | CharField(100) | Patient's name |
| `date_of_birth` | DateField | Used to compute age via `@property` |
| `gender` | CharField (choices) | `M` / `F` / `O` |
| `blood_group` | CharField (choices) | `A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-` |
| `phone` | CharField(15) | Primary contact |
| `registration_type` | CharField (choices) | `OPD` (Out-Patient) / `IPD` (In-Patient) |
| `allergies` | TextField | Known allergies (comma-separated) |
| `chronic_conditions` | TextField | Diabetes, hypertension, etc. |
| `past_surgeries` | TextField | Previous surgical history |
| `emergency_contact_name` / `_phone` | CharField | Emergency contact details |
| `is_active` | BooleanField | Soft-delete flag |
| `registered_on` | DateTimeField (auto) | Registration timestamp |

**Auto-ID Logic:**
```python
def save(self, *args, **kwargs):
    if not self.patient_id:
        last = Patient.objects.order_by('-id').first()
        num = (last.id + 1) if last else 1
        self.patient_id = f'CURA-P{num:05d}'
    super().save(*args, **kwargs)
```

---

#### 3. **Doctor** (`doctors/models.py`)
Doctor profile linked one-to-one with User.

| Field | Type | Description |
|---|---|---|
| `doctor_id` | CharField (auto) | Format: `CURA-D0001` |
| `specialization` | CharField (choices) | 12 options: General Medicine, Cardiology, Neurology, etc. |
| `qualification` | CharField(200) | e.g., "MBBS, MD (Cardiology)" |
| `experience_years` | PositiveInteger | Years of clinical experience |
| `consultation_fee` | Decimal(8,2) | Per-visit fee in ₹ |
| `available_days` | CharField(100) | Comma-separated: `mon,tue,wed` |
| `available_from` / `_to` | TimeField | Duty hours (e.g., 09:00–17:00) |
| `bio` | TextField | Short professional biography |
| `is_available` | BooleanField | Currently accepting appointments |

---

#### 4. **Appointment** (`appointments/models.py`)
Core operational model linking patients and doctors on specific time slots.

| Field | Type | Description |
|---|---|---|
| `appointment_id` | CharField (auto) | Format: `CURA-A000001` |
| `patient` | ForeignKey → Patient | The patient being seen |
| `doctor` | ForeignKey → Doctor | The doctor conducting the visit |
| `date` | DateField | Appointment date |
| `time_slot` | CharField (choices) | 14 slots from `09:00` to `16:30` (30-min intervals) |
| `status` | CharField (choices) | `pending` → `confirmed` → `in_progress` → `completed` → `cancelled` |
| `reason` | TextField | Reason for visit |
| `diagnosis` | TextField | Doctor's diagnosis (filled during/after visit) |
| `notes` | TextField | Additional doctor's notes |

**Constraint:** `unique_together = ['doctor', 'date', 'time_slot']` — prevents double-booking.

**Status color mapping** (for UI badges):
```python
@property
def status_color(self):
    colors = {
        'pending': 'warning',
        'confirmed': 'info',
        'in_progress': 'primary',
        'completed': 'success',
        'cancelled': 'danger',
    }
    return colors.get(self.status, 'secondary')
```

---

#### 5. **Medicine** (`pharmacy/models.py`)
Medicine inventory with stock level alerts.

| Field | Type | Description |
|---|---|---|
| `name` | CharField(200) | Brand name |
| `generic_name` | CharField(200) | Generic/chemical name |
| `category` | CharField (choices) | Tablet, Capsule, Syrup, Injection, Ointment, Drops, Inhaler, Other |
| `manufacturer` | CharField(200) | Pharma company |
| `price` | Decimal(10,2) | Unit price in ₹ |
| `quantity_in_stock` | PositiveInteger | Current stock count |
| `reorder_level` | PositiveInteger | Threshold for low-stock alert (default: 10) |
| `expiry_date` | DateField | Expiry date for batch tracking |

**Properties:** `is_low_stock` (stock ≤ reorder level), `is_expired` (expiry ≤ today)

---

#### 6. **Prescription** & **PrescriptionItem** (`pharmacy/models.py`)
Digital prescriptions linked to appointments.

**Prescription:**
| Field | Type | Description |
|---|---|---|
| `appointment` | OneToOneField → Appointment | One prescription per appointment |
| `notes` | TextField | Additional instructions |

**PrescriptionItem** (medicines in the prescription):
| Field | Type | Description |
|---|---|---|
| `medicine` | ForeignKey → Medicine | Which medicine |
| `dosage` | CharField (choices) | `1-0-0` (morning only), `1-1-1` (three times), `SOS`, etc. |
| `duration_days` | PositiveInteger | Number of days |
| `quantity` | PositiveInteger | Total quantity |
| `instructions` | CharField(200) | e.g., "After food", "Before sleep" |

---

#### 7. **Invoice** & **InvoiceItem** (`billing/models.py`)
Financial tracking per appointment.

**Invoice:**
| Field | Type | Description |
|---|---|---|
| `invoice_id` | CharField (auto) | Format: `CURA-INV00001` |
| `appointment` | OneToOneField → Appointment | One invoice per appointment |
| `total_amount` | Decimal(10,2) | Sum of all line items |
| `discount` | Decimal(10,2) | Discount applied |
| `paid_amount` | Decimal(10,2) | Amount paid so far |
| `status` | CharField (choices) | `unpaid`, `partial`, `paid` |

**Properties:** `net_amount` (total - discount), `due_amount` (net - paid), `status_color`

---

#### 8. **Ward** & **Bed** (`wards/models.py`)
Physical infrastructure management.

**Ward:**
| Field | Type | Description |
|---|---|---|
| `name` | CharField(100) | e.g., "General Ward A" |
| `ward_type` | CharField (choices) | General, Semi-Private, Private, ICU, NICU, OT |
| `floor` | PositiveInteger | Building floor number |
| `capacity` | PositiveInteger | Number of beds |
| `charge_per_day` | Decimal(10,2) | Daily bed charge in ₹ |

**Properties:** `occupied_beds`, `available_beds`, `occupancy_percentage`

**Bed:**
| Field | Type | Description |
|---|---|---|
| `ward` | ForeignKey → Ward | Which ward this bed belongs to |
| `bed_number` | CharField(10) | e.g., "01", "02" |
| `status` | CharField (choices) | `available`, `occupied`, `reserved`, `maintenance` |
| `patient` | ForeignKey → Patient (nullable) | Currently admitted patient |
| `admitted_on` | DateTimeField (nullable) | Admission timestamp |

---

## 📦 Module-wise Description

### 1. Core Module — Authentication & Dashboard

**Purpose:** User authentication, role management, and the central dashboard.

**Models:**
- `User` — Custom user model extending `AbstractUser` with `role`, `phone`, `profile_pic`, `address`
- `Notification` — Simple notification model (title, message, is_read, icon)

**Views:**

| View | URL | Method | Description |
|---|---|---|---|
| `home_view` | `/` | GET | Landing page — redirects to dashboard if logged in |
| `login_view` | `/login/` | GET/POST | Custom login with styled form |
| `logout_view` | `/logout/` | GET | Logout and redirect to login |
| `dashboard_view` | `/dashboard/` | GET | Role-based dashboard with analytics |
| `profile_view` | `/profile/` | GET/POST | Edit user profile |
| `mark_notification_read` | `/notification/<pk>/read/` | GET | Mark notification as read |

**Dashboard Analytics (computed in view):**
- Total active patients, available doctors
- Today's appointments, pending appointments
- Total revenue collected, unpaid invoices
- Available/occupied beds, low-stock medicines
- Weekly appointment data (for Chart.js bar chart)
- Status distribution (for Chart.js doughnut chart)
- Ward occupancy data

---

### 2. Patients Module

**Purpose:** Complete patient lifecycle management — registration, medical history, and tracking.

**Views:**

| View | URL | Method | Description |
|---|---|---|---|
| `patient_list` | `/patients/` | GET | Searchable, filterable patient table |
| `patient_add` | `/patients/add/` | GET/POST | Multi-section registration form |
| `patient_detail` | `/patients/<pk>/` | GET | Profile card + medical history + appointment history |
| `patient_edit` | `/patients/<pk>/edit/` | GET/POST | Edit patient information |
| `patient_delete` | `/patients/<pk>/delete/` | GET/POST | Soft-delete (sets `is_active=False`) |

**Search & Filter:** Patients can be searched by name, patient ID, or phone number. Filtered by registration type (OPD/IPD).

**Form Sections:**
1. Personal Information (name, DOB, gender, blood group, phone, email, address)
2. Emergency Contact (name, phone)
3. Medical Details (registration type, allergies, chronic conditions, past surgeries)

---

### 3. Doctors Module

**Purpose:** Doctor profile management with specialization and availability tracking.

**Views:**

| View | URL | Method | Description |
|---|---|---|---|
| `doctor_list` | `/doctors/` | GET | Card-based grid with specialization badges |
| `doctor_detail` | `/doctors/<pk>/` | GET | Full profile + recent appointments |
| `doctor_edit` | `/doctors/<pk>/edit/` | GET/POST | Edit doctor + linked user info |

**Display:** Doctors are shown as cards (not table rows) with avatar initials, specialization badges, availability status, experience, and consultation fee.

---

### 4. Appointments Module

**Purpose:** Appointment booking, status management, and the workflow pipeline.

**Views:**

| View | URL | Method | Description |
|---|---|---|---|
| `appointment_list` | `/appointments/` | GET | Full table with status filter pills |
| `appointment_add` | `/appointments/add/` | GET/POST | Booking form (patient, doctor, date, time slot) |
| `appointment_detail` | `/appointments/<pk>/` | GET | Info card + journey tracker + quick actions |
| `appointment_update` | `/appointments/<pk>/update/` | GET/POST | Update status, diagnosis, notes |
| `appointment_cancel` | `/appointments/<pk>/cancel/` | GET/POST | Cancel with confirmation |

**Status Workflow:**
```
pending → confirmed → in_progress → completed
    └──────────────────────────────→ cancelled
```

**Unique:** Each appointment detail page shows a **per-appointment workflow tracker** — a visual step indicator showing exactly where this appointment is in the pipeline.

**Quick Actions from Appointment Detail:**
- Update Status
- Write Prescription (links to pharmacy module)
- Generate Invoice (links to billing module)
- Cancel Appointment

**Double-Booking Prevention:** The model enforces `unique_together = ['doctor', 'date', 'time_slot']`.

---

### 5. Pharmacy Module

**Purpose:** Medicine inventory management and digital prescription writing.

**Views:**

| View | URL | Method | Description |
|---|---|---|---|
| `medicine_list` | `/pharmacy/` | GET | Inventory table with category filter, low-stock alerts |
| `medicine_add` | `/pharmacy/add/` | GET/POST | Add new medicine to inventory |
| `medicine_edit` | `/pharmacy/<pk>/edit/` | GET/POST | Edit medicine details |
| `prescription_create` | `/pharmacy/prescription/create/<apt_pk>/` | GET/POST | Write prescription for an appointment |
| `prescription_detail` | `/pharmacy/prescription/<pk>/` | GET | Print-ready prescription with branded header |

**Low-Stock Alert:** Medicines with `quantity_in_stock ≤ reorder_level` are flagged on both the pharmacy page and the dashboard.

**Prescription Form:** Uses Django's `inlineformset_factory` to allow adding multiple medicines in one form submission.

**Dosage Patterns:** `1-0-0` (morning), `0-1-0` (afternoon), `1-1-1` (thrice daily), `SOS` (as needed), etc.

**Print-Ready Prescription:** Branded header with CURA logo, patient info, doctor info, medicine table, and print button (CSS `@media print` hides navigation).

---

### 6. Billing Module

**Purpose:** Invoice generation, line items, and payment tracking.

**Views:**

| View | URL | Method | Description |
|---|---|---|---|
| `invoice_list` | `/billing/` | GET | Invoice table with status filter (Unpaid/Partial/Paid) |
| `invoice_create` | `/billing/create/<apt_pk>/` | GET/POST | Generate invoice from appointment |
| `invoice_detail` | `/billing/<pk>/` | GET | Print-ready invoice with totals |
| `invoice_pay` | `/billing/<pk>/pay/` | GET/POST | Record a payment |

**Auto-Calculation:** When an invoice is created, the doctor's consultation fee is automatically added. Additional line items (lab tests, medicines, procedures) can be added via the inline formset.

**Payment Flow:**
1. Invoice starts as `unpaid`
2. Partial payments → status becomes `partial`
3. When `paid_amount ≥ net_amount` → status becomes `paid`

**Print-Ready Invoice:** Branded header, patient/doctor info, itemised table, subtotal/discount/net/paid/due breakdown, and print button.

---

### 7. Wards & Beds Module

**Purpose:** Physical bed management with visual occupancy tracking.

**Views:**

| View | URL | Method | Description |
|---|---|---|---|
| `ward_list` | `/wards/` | GET | Ward cards with occupancy bar + bed grid |
| `ward_add` | `/wards/add/` | GET/POST | Create ward (beds auto-generated) |
| `ward_detail` | `/wards/<pk>/` | GET | Bed-by-bed management table |
| `bed_admit` | `/wards/bed/<pk>/admit/` | POST | Admit a patient to a bed |
| `bed_discharge` | `/wards/bed/<pk>/discharge/` | POST | Discharge a patient from a bed |

**Auto-Bed Creation:** When a ward is created with capacity N, N beds are automatically generated:
```python
for i in range(1, ward.capacity + 1):
    Bed.objects.create(ward=ward, bed_number=f'{i:02d}')
```

**Visual Bed Occupancy Grid:** Each ward card on the list page shows a CSS grid of bed cells, color-coded:
- 🟢 Green = Available
- 🔴 Red = Occupied
- 🟡 Yellow = Reserved
- ⚫ Grey = Under Maintenance

**Admit/Discharge:** The ward detail page shows a table where staff can:
- Select an IPD patient from a dropdown and admit them to an available bed
- Discharge an occupied bed (with confirmation)

---

## 🔗 URL Routing

### Root URLs (`hospital_management/urls.py`)

| Pattern | Include | Namespace |
|---|---|---|
| `admin/` | Django admin | — |
| ` ` (root) | `core.urls` | — |
| `patients/` | `patients.urls` | `patients` |
| `doctors/` | `doctors.urls` | `doctors` |
| `appointments/` | `appointments.urls` | `appointments` |
| `pharmacy/` | `pharmacy.urls` | `pharmacy` |
| `billing/` | `billing.urls` | `billing` |
| `wards/` | `wards.urls` | `wards` |

### All Application URLs

| App | URL | Name | View |
|---|---|---|---|
| **Core** | `/` | `home` | Landing page |
| | `/login/` | `login` | Login |
| | `/logout/` | `logout` | Logout |
| | `/dashboard/` | `dashboard` | Dashboard |
| | `/profile/` | `profile` | User profile |
| **Patients** | `/patients/` | `patients:patient_list` | Patient list |
| | `/patients/add/` | `patients:patient_add` | Register patient |
| | `/patients/<pk>/` | `patients:patient_detail` | Patient profile |
| | `/patients/<pk>/edit/` | `patients:patient_edit` | Edit patient |
| | `/patients/<pk>/delete/` | `patients:patient_delete` | Deactivate |
| **Doctors** | `/doctors/` | `doctors:doctor_list` | Doctor grid |
| | `/doctors/<pk>/` | `doctors:doctor_detail` | Doctor profile |
| | `/doctors/<pk>/edit/` | `doctors:doctor_edit` | Edit doctor |
| **Appointments** | `/appointments/` | `appointments:appointment_list` | Appointment list |
| | `/appointments/add/` | `appointments:appointment_add` | Book appointment |
| | `/appointments/<pk>/` | `appointments:appointment_detail` | Detail + tracker |
| | `/appointments/<pk>/update/` | `appointments:appointment_update` | Update status |
| | `/appointments/<pk>/cancel/` | `appointments:appointment_cancel` | Cancel |
| **Pharmacy** | `/pharmacy/` | `pharmacy:medicine_list` | Medicine inventory |
| | `/pharmacy/add/` | `pharmacy:medicine_add` | Add medicine |
| | `/pharmacy/<pk>/edit/` | `pharmacy:medicine_edit` | Edit medicine |
| | `/pharmacy/prescription/create/<apt_pk>/` | `pharmacy:prescription_create` | Write Rx |
| | `/pharmacy/prescription/<pk>/` | `pharmacy:prescription_detail` | View Rx |
| **Billing** | `/billing/` | `billing:invoice_list` | Invoice list |
| | `/billing/create/<apt_pk>/` | `billing:invoice_create` | Generate invoice |
| | `/billing/<pk>/` | `billing:invoice_detail` | View invoice |
| | `/billing/<pk>/pay/` | `billing:invoice_pay` | Record payment |
| **Wards** | `/wards/` | `wards:ward_list` | Ward list |
| | `/wards/add/` | `wards:ward_add` | Add ward |
| | `/wards/<pk>/` | `wards:ward_detail` | Manage beds |
| | `/wards/bed/<pk>/admit/` | `wards:bed_admit` | Admit patient |
| | `/wards/bed/<pk>/discharge/` | `wards:bed_discharge` | Discharge |

---

## 🎭 Template System

CURA uses Django's **template inheritance** system with a single master layout:

```
base.html                ← Master layout (sidebar + topbar + messages)
  ├── core/home.html     ← Standalone (no sidebar — landing page)
  ├── core/login.html    ← Standalone (no sidebar — login page)
  ├── core/dashboard.html  ← Extends base.html
  ├── core/profile.html    ← Extends base.html
  ├── patients/...         ← All extend base.html
  ├── doctors/...          ← All extend base.html
  └── ...
```

### `base.html` provides:
1. **HTML `<head>`** — Meta tags, Bootstrap CSS, Bootstrap Icons, CURA CSS, Chart.js
2. **Sidebar** — Fixed left navigation with CURA branding, section titles, nav links with active state detection, and sign-out
3. **Topbar** — Glassmorphic top bar with page title, user avatar pill (initials + name + role)
4. **Messages** — Django messages framework with Bootstrap alerts and animated slide-in
5. **Content area** — `{% block content %}` for child templates
6. **Scripts** — Bootstrap JS, Chart.js, `{% block extra_js %}` for page-specific scripts

### Template Blocks:
- `{% block title %}` — Page title in `<title>` tag
- `{% block page_title %}` — Displayed in the topbar
- `{% block content %}` — Main page content
- `{% block extra_css %}` — Additional stylesheets
- `{% block extra_js %}` — Additional scripts (e.g., Chart.js initialization)

---

## 🎨 UI/UX Design Philosophy

### Color Palette

| Token | Color | Hex | Usage |
|---|---|---|---|
| `--cura-pink-lightest` | Very light pink | `#FFF5F7` | Page background |
| `--cura-pink-light` | Light pink | `#FFF0F3` | Card backgrounds, form backgrounds |
| `--cura-pink` | Soft pink | `#FFD6E0` | Borders, separators |
| `--cura-rose` | Rose | `#FF7FA5` | Hover states, accents |
| `--cura-red` | Soothing red | `#C0392B` | Primary brand color, buttons, sidebar |
| `--cura-red-light` | Light red | `#E74C3C` | Gradients, highlights |
| `--cura-red-dark` | Dark red | `#96281B` | Sidebar gradient bottom, hover states |
| `--cura-white` | Pure white | `#FFFFFF` | Cards, inputs |

### Typography
- **Font family:** Poppins (Google Fonts) — weights 300, 400, 500, 600, 700
- **Headings:** Weight 600–700, color `--cura-gray-900`
- **Body:** Weight 400, color `--cura-gray-700`
- **Small labels:** Weight 500, color `--cura-gray-500`, uppercase letter-spacing

### Design Components
- **Stat Cards** — Rounded corners, top color stripe (gradient), hover lift animation
- **CURA Cards** — White cards with pink border, pink header background
- **Buttons** — Three variants: `btn-cura` (gradient fill), `btn-cura-outline`, `btn-cura-soft` (pastel fill)
- **Tables** — Custom `cura-table` with pink header row, hover highlighting
- **Badges** — Rounded, soft background with text color matching status
- **Search** — Rounded input with search icon overlay
- **Forms** — Custom focus ring (pink glow)

### Animations
- `fadeInUp` — Cards animate in on page load with staggered delays
- `slideDown` — Alert messages slide in from top
- Hover lift — Cards translate up 4px on hover
- Button hover — Translate up 2px + enhanced shadow

### Responsive Design
- Sidebar collapses to off-canvas on screens < 992px
- Stat cards stack to 2-column on mobile
- Tables become horizontally scrollable
- Login card adds margin on mobile

### Print Styles
- Sidebar, topbar, and buttons are hidden
- Background set to white
- Card shadows removed, borders added

---

## ✨ Unique Features (What Makes CURA Different)

### 1. OPD Workflow Tracker
A visual step-by-step pipeline showing the patient journey:
```
Register → Appointment → Diagnosis → Prescription → Billing → Discharge
```
Shown on the dashboard (global view) and on each appointment detail page (specific to that appointment). Steps are color-coded: ✅ green (completed), 🔴 red (active), ⚪ grey (pending).

### 2. Visual Bed Occupancy Map
Instead of a plain table, wards display an **interactive CSS grid** of bed cells. Each cell is color-coded by status and shows the bed number. Hovering reveals patient info for occupied beds.

### 3. Humanised Copy
Every page uses warm, empathetic language:
- *"Every person here trusts us with their care. Let's honour that."* (Patients page)
- *"The heartbeat of CURA — dedicated professionals who make it all possible."* (Doctors page)
- *"Every visit is a step toward healing. Let's keep things organised."* (Appointments page)
- *"No appointments this week yet. Things are peaceful! 🌸"* (Empty state)
- *"Hmm, that didn't work. Please check your username and password."* (Login error)

### 4. Auto-Generated Branded IDs
Every entity has a unique, human-readable ID:
- Patients: `CURA-P00001`
- Doctors: `CURA-D0001`
- Appointments: `CURA-A000001`
- Invoices: `CURA-INV00001`

### 5. Print-Ready Documents
Prescriptions and invoices feature:
- Branded gradient header with CURA logo
- Patient and doctor information
- Itemised table
- Print button that triggers `window.print()`
- CSS `@media print` rules hide navigation

### 6. Chart.js Dashboard Analytics
- **Bar chart** — Appointments per day for the current week
- **Doughnut chart** — Appointment status distribution (pending/confirmed/in_progress/completed/cancelled)

### 7. Time-Aware Greeting
Dashboard greets users based on the current time:
- Morning (before 12:00): "Good morning, Arjun! 👋"
- Afternoon (12:00–17:00): "Good afternoon, Arjun! 👋"
- Evening (after 17:00): "Good evening, Arjun! 👋"

### 8. Glassmorphic UI Elements
Login card and topbar use `backdrop-filter: blur()` for a frosted-glass effect.

---

## 🔄 OPD Workflow — The Patient Journey

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   STEP 1     │     │   STEP 2     │     │   STEP 3     │
│  REGISTER    │────▶│  APPOINTMENT │────▶│  DIAGNOSIS   │
│  Patient     │     │  Book a slot │     │  Doctor sees │
│  /patients/  │     │  /appoint../ │     │  the patient │
│  add/        │     │  add/        │     │  /update/    │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
                                                 ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   STEP 6     │     │   STEP 5     │     │   STEP 4     │
│  DISCHARGE   │◀────│   BILLING    │◀────│ PRESCRIPTION │
│  (if IPD)    │     │  Generate    │     │  Write Rx    │
│  /wards/bed/ │     │  invoice     │     │  /pharmacy/  │
│  discharge/  │     │  /billing/   │     │  prescription│
└──────────────┘     └──────────────┘     └──────────────┘
```

### How It Works End-to-End:

1. **Register** — Receptionist creates a patient record via `/patients/add/`. An auto-ID like `CURA-P00003` is assigned.

2. **Book Appointment** — Receptionist selects the patient, chooses a doctor, picks a date and time slot. The appointment starts as `pending`.

3. **Confirm & Diagnose** — The doctor (or receptionist) updates the appointment status to `confirmed`, then `in_progress`. The doctor fills in the diagnosis and notes.

4. **Write Prescription** — From the appointment detail page, the doctor clicks "Write Prescription" and selects medicines with dosage patterns. This creates a digital, printable prescription.

5. **Generate Invoice** — From the same appointment detail page, staff clicks "Generate Invoice". The doctor's consultation fee is auto-added. Additional line items (lab tests, etc.) can be added. Payment can be recorded immediately or later.

6. **Discharge** — If the patient was admitted (IPD), staff navigates to Wards & Beds, finds the occupied bed, and clicks "Discharge". The bed returns to `available` status.

---

## 🖥 Screenshots

*(The application is currently running at http://127.0.0.1:8000/ — log in with `admin` / `admin123` to see all pages.)*

### Key Pages:
- **Landing Page** — Hero section with "Healthcare, made human again" tagline
- **Login** — Glassmorphic card with CURA branding on pink gradient background
- **Dashboard** — 6 stat cards, OPD workflow tracker, bar chart, doughnut chart, recent appointments table
- **Patients** — Searchable table with CURA IDs, blood group badges, OPD/IPD type badges
- **Doctors** — Card grid with avatar initials, specialization, availability
- **Appointments** — Status filter pills (All/Pending/Confirmed/...), color-coded status badges
- **Appointment Detail** — Per-appointment journey tracker, quick action buttons
- **Pharmacy** — Medicine inventory with low-stock warnings, category badges
- **Prescription** — Print-ready document with branded header
- **Billing** — Invoice list with due amounts highlighted, payment status
- **Invoice Detail** — Print-ready with itemised breakdown
- **Wards** — Ward cards with occupancy progress bar + visual bed grid
- **Ward Detail** — Bed-by-bed table with admit/discharge actions

---

## ⚙ Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Step-by-Step

```bash
# 1. Navigate to the project directory
cd c:\_Work_\WPL

# 2. Install dependencies
pip install django

# 3. Apply database migrations
python manage.py makemigrations
python manage.py migrate

# 4. Seed demo data (creates users, patients, doctors, appointments, medicines, wards, etc.)
python manage.py seed_data

# 5. Start the development server
python manage.py runserver

# 6. Open in browser
# http://127.0.0.1:8000/
```

### What `seed_data` Creates:
- **1 Admin** user (`admin` / `admin123`)
- **1 Receptionist** user (`receptionist` / `recep123`)
- **5 Doctors** with different specializations (Cardiology, Orthopedics, Pediatrics, Neurology, Dermatology)
- **8 Patients** with varying demographics, blood groups, and medical histories
- **10 Medicines** across categories (Tablet, Capsule, Syrup, Injection, etc.)
- **8 Appointments** (mix of pending, confirmed, completed)
- **Prescriptions** for completed appointments
- **Invoices** (paid) for completed appointments
- **5 Wards** (General A, General B, Private Wing, ICU, Pediatric) with beds
- **3 IPD patients admitted** to beds
- **2 beds** marked as under maintenance

---

## 🔑 Demo Credentials

| Role | Username | Password | What They Can See |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Full access — all modules, admin panel |
| **Receptionist** | `receptionist` | `recep123` | All modules (no admin panel access) |
| **Doctor** | `dr.ananya` | `doctor123` | All modules (would see own appointments in a role-filtered version) |
| **Doctor** | `dr.rahul` | `doctor123` | Same as above |
| **Doctor** | `dr.meera` | `doctor123` | Same as above |
| **Doctor** | `dr.vikram` | `doctor123` | Same as above |
| **Doctor** | `dr.sana` | `doctor123` | Same as above |

---

## 🔮 Future Enhancements

1. **Role-based view filtering** — Doctors see only their appointments; patients see only their records.
2. **REST API** — Django REST Framework for mobile app integration.
3. **Email/SMS notifications** — Appointment reminders and prescription delivery.
4. **Lab reports module** — Upload and manage diagnostic reports.
5. **Inventory auto-deduction** — Reduce medicine stock when prescriptions are dispensed.
6. **Advanced analytics** — Monthly/quarterly reports, doctor performance metrics, revenue trends.
7. **Multi-hospital support** — Branch management for hospital chains.
8. **Patient portal** — Self-service appointment booking and medical history access.
9. **Dark mode** — Toggle between light and dark themes.

---

## 📌 Conclusion

**CURA** demonstrates a production-quality approach to hospital management system design. It covers the full operational lifecycle of a hospital — from patient intake to financial settlement — while maintaining a **warm, humanised interface** that respects the people behind the data.

### Key Technical Highlights:
- **7 Django apps** with clean separation of concerns
- **12 database models** with proper relationships (FK, OneToOne, unique constraints)
- **25+ views** covering CRUD operations, status workflows, and analytics
- **27 HTML templates** with inheritance from a single `base.html`
- **500+ lines of custom CSS** implementing a cohesive design system
- **Auto-generated branded IDs** across all entities
- **Chart.js integration** for real-time dashboard analytics
- **Management command** for one-command demo data seeding
- **Print-ready documents** for prescriptions and invoices
- **Responsive design** supporting desktop, tablet, and mobile

CURA proves that a hospital management system doesn't have to feel cold and clinical — it can be **beautiful, intuitive, and deeply human**.

---

*Built with ❤️ using Django, Bootstrap, and a lot of empathy.*
