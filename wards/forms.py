from django import forms
from .models import Ward, Bed


class WardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ['name', 'ward_type', 'floor', 'capacity', 'charge_per_day', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ward_type': forms.Select(attrs={'class': 'form-select'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'charge_per_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['ward', 'bed_number', 'status', 'notes']
        widgets = {
            'ward': forms.Select(attrs={'class': 'form-select'}),
            'bed_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class AdmitPatientForm(forms.Form):
    patient = forms.IntegerField(widget=forms.Select(attrs={'class': 'form-select'}))
