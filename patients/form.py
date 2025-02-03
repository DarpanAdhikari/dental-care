from django import forms
from accounts.models import Patient
from django.core.exceptions import ValidationError

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient 
        fields = ['phone','address','medical_history']
        widgets = {
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your address'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Any medical history'}),
        }