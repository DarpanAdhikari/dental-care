from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Appointment, Prescription
from .form import PrescriptionForm
from administration.form import DoctorForm 
from accounts.form import UserForm,UserChangeForm
from accounts.models import Doctor
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db.models import Count

def staff_required(user):
    return user.is_staff and not user.is_superuser

@login_required
@user_passes_test(staff_required, login_url='/accounts/login/')
def doctors_info(request):
    doctor = get_object_or_404(Doctor, user=request.user.id)
    patients = Appointment.objects.filter(doctor=doctor).values('patient_id').distinct().count()
    totalApointment = Appointment.objects.filter(doctor=doctor).count()
    totalPrescription = Prescription.objects.filter(appointment__doctor=doctor).count()
    appointment_counts = Appointment.objects.filter(doctor=doctor).values('status').annotate(count=Count('status'))
    status_counts = {item['status']: item['count'] for item in appointment_counts}
    appointmentCounter = {
        'totalPending': status_counts.get('pending', 0),
        'totalConfirm': status_counts.get('confirmed', 0),
        'totalCancel': status_counts.get('cancelled', 0),
        'totalComplete': status_counts.get('completed',0)
    }
    return render(request, 'doctor_index.html',{'totalPatient':patients,'totalApointment':totalApointment,\
        'totalPrescription':totalPrescription,'appointmentCounter':appointmentCounter})

@login_required
@user_passes_test(staff_required, login_url='/accounts/login/')
def view_appointment(request):
    doctor = Doctor.objects.filter(user=request.user).first()
    appointments = Appointment.objects.filter(doctor=doctor,status='pending').exclude(status__in=['cancelled', 'confirmed'])
    return render(request, 'patient_appointment.html', {'appointments': appointments})

@login_required
@user_passes_test(staff_required, login_url='/accounts/login/')
def confirm_appointment(request,app_id):
    appointment = Appointment.objects.filter(id=app_id).filter()
    if appointment:
        appointment.update(status='confirmed')
        messages.success(request,"Appointment confirmed successfully")
    return redirect('doctors_appointment')

@login_required
@user_passes_test(staff_required, login_url='/accounts/login/')
def cancel_appointment(request,app_id):
    appointment = Appointment.objects.filter(id=app_id).filter()
    if appointment:
        appointment.update(status='cancelled')
        messages.success(request,"Appointment cancelled successfully")
    return redirect('doctors_appointment')

@login_required
@user_passes_test(staff_required, login_url='/accounts/login/')
def manage_prescription(request,app_id=None):
    form = PrescriptionForm()
    appointments = Appointment.objects.filter(status='confirmed')
    if app_id:
        if request.method == 'POST':
            form = PrescriptionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Prescription for this patient is submited!")
                return render(request,'doctor_prescription.html',{'appointments':appointments})
        return render(request,'doctor_prescription.html',{'appointments':appointments,'form':form,'app_id':app_id})
    return render(request,'doctor_prescription.html',{'appointments':appointments})

@login_required
@user_passes_test(staff_required, login_url='/accounts/login/')
def edit_profile(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    if request.method == 'POST':
        doctForm = DoctorForm(request.POST, request.FILES, instance=doctor)
        userForm = UserChangeForm(request.POST, instance=doctor.user)
        if doctForm.is_valid() and userForm.is_valid():
            userForm.save()
            doctor = doctForm.save(commit=False)
            doctor.save()
            doctForm.save_m2m()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('edit_profile')
    else:
        doctForm = DoctorForm(instance=doctor)
        userForm = UserChangeForm(instance=doctor.user)

    return render(request, 'doctors_profile.html', {'doctorForm': doctForm, 'userForm': userForm})
