from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .form import AppointmentForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from accounts.models import Patient,Doctor
from administration.models import DentalPost
def index(request):
    doctors = Doctor.objects.all()
    posts = DentalPost.objects.all().order_by('-id')
    appointment = AppointmentForm()
    return render(request,'index.html',{'appointForm':appointment,'doctors':doctors,'posts':posts})

@login_required
def create_appointment(request):
    appointment = AppointmentForm()
    errors = None
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            messages.error(request, "Please login with patient credentials to reserve appointment.")
            return redirect(reverse('home'))
    if request.method == 'POST':
        appointmentForm = AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            patientInstance = Patient.objects.filter(user=request.user).first()
            appointmentForm.instance.patient = patientInstance
            appointmentForm.save()
            return redirect('dashboard')
        else:
            errors = appointmentForm.errors.as_data()
            messages.error(request, "Appointment form invalid!")
    return render(request, 'index.html', {'appointForm': appointment,'errors':errors})
