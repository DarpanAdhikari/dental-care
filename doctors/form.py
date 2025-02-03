from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['appointment', 'diagnosis', 'medicines', 'advice']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3,'class':'form-control','placeholder':'Enter diagnosis details..'}),
            'medicines': forms.Textarea(attrs={'rows': 3,'class':'form-control','placeholder':'List prescribed medicines'}),
            'advice': forms.Textarea(attrs={'rows': 3,'class':'form-control','placeholder':'Provide advice for the patient'}),
        }