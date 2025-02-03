from doctors.models import Appointment
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient','doctor', 'appointment_date']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select form-control-lg'}),
            'doctor': forms.Select(attrs={'class': 'form-select form-control-lg'}),
            'appointment_date': forms.DateTimeInput(
                attrs={'class': 'form-control form-control-lg futureDate', 'type': 'datetime-local'}
            ),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        if appointment_date <= timezone.make_aware(datetime.now()):
            raise ValidationError("Appointment date and time must be in the future.")
        if not (10 <= appointment_date.hour < 18):
            raise ValidationError("Appointment time must be between 10:00 AM and 6:00 PM.")
        return appointment_date