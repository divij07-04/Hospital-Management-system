from django import forms
from .models import Doctor
from core.models import User


class DoctorForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        model = Doctor
        fields = [
            'specialization', 'qualification', 'experience_years',
            'consultation_fee', 'available_days', 'available_from',
            'available_to', 'bio', 'is_available',
        ]
        widgets = {
            'specialization': forms.Select(attrs={'class': 'form-select'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mon,tue,wed,thu,fri'}),
            'available_from': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'available_to': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
