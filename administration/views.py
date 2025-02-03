from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required,permission_required
from .form import *
from accounts.form import UserForm, UserChangeForm
from patients.form import PatientForm
from frontend.form import AppointmentForm
from accounts.models import Doctor,Patient
from doctors.models import Appointment,Bill,Prescription
from django.contrib.auth.models import User
import random
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.contrib import messages
from django.db.models import Count

def generate_random_number():
    part1 = str(random.randint(0, 9999)).zfill(4)
    part2 = str(random.randint(0, 9999)).zfill(4)
    return f"{part1}-{part2}"

def get_unique_user_id():
    while True:
        user_id = generate_random_number()
        if not User.objects.filter(username=user_id).exists():
            return user_id
        
@login_required
@permission_required('auth', raise_exception=True)
def admin_index(request):
    totalPatient = Patient.objects.all().count()
    totalApointment = Appointment.objects.all().count()
    totalAmount = Bill.objects.aggregate(Sum('amount'))['amount__sum']
    busy_doctor = (Appointment.objects.values('doctor').annotate(count=Count('doctor'))
                    .order_by('-count').first())
    if busy_doctor:
        doctor_id = busy_doctor['doctor']
        busiest_doctor = Doctor.objects.get(id=doctor_id)
    appointment_counts = Appointment.objects.values('status').annotate(count=Count('status'))
    status_counts = {item['status']: item['count'] for item in appointment_counts}
    appointmentCounter = {
        'totalPending': status_counts.get('pending', 0),
        'totalConfirm': status_counts.get('confirmed', 0),
        'totalCancel': status_counts.get('cancelled', 0),
        'totalComplete': status_counts.get('completed',0)
    }
    return render(request,'admin_index.html',{'totalPatient':totalPatient,'totalApointment':totalApointment,\
          'totalAmount':totalAmount,'appointmentCounter':appointmentCounter,'busyDoctor':busiest_doctor})
    

@login_required
@permission_required('auth', raise_exception=True)
def doctor_form(request, user_id=None):
    doctors = Doctor.objects.all()
    for doctor in doctors:
        appointments = Appointment.objects.filter(doctor=doctor, status__in=['pending', 'confirmed','completed','cancelled'])
        doctor.pending_count = appointments.filter(status='pending').count()
        doctor.cancelled_count = appointments.filter(status='cancelled').count()
        doctor.completed_count = appointments.filter(status='completed').count()
        doctor.confirmed_count = appointments.filter(status='confirmed').count()
    doctor = None
    userInfo = None
    is_edit_mode = False 
    if user_id: 
        doctor = Doctor.objects.filter(id=user_id).first()
        userInfo = User.objects.filter(id=doctor.user.id).first()
        if doctor:
            is_edit_mode = True 
    if request.method == 'POST':
        doctForm = DoctorForm(request.POST, instance=doctor)
        userForm = UserForm(request.POST, instance=userInfo)
        if is_edit_mode:
            userForm = UserChangeForm(request.POST,instance=userInfo)
        if doctForm.is_valid() and userForm.is_valid():
            user = userForm.save(commit=False)
            if not is_edit_mode: 
                user.is_staff = True
                user.username = get_unique_user_id()
            user.save()
            doctor = doctForm.save(commit=False)
            doctor.user = user
            doctor.save()
            doctForm.save_m2m()
            return redirect('doctor_mng')
    else:
        doctForm = DoctorForm(instance=doctor)
        userForm = UserForm(instance=userInfo)

    return render(request, 'doctors_form.html', {'doctorForm': doctForm, 'userForm': userForm,'doctors':doctors,'is_edit_mode':is_edit_mode})

@login_required
@permission_required('auth', raise_exception=True)
def delete_doctor(request):
    id = request.POST.get('user')
    if not request.user.is_superuser:
        raise PermissionDenied
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect(reversed('doctor_mng'))


@login_required
@permission_required('auth', raise_exception=True)
def patient_form(request,user_id=None):
    patients = Patient.objects.all()
    patient = None
    userInfo = None
    is_edit_mode = False 
    if user_id: 
        patient = Patient.objects.filter(id=user_id).first()
        userInfo = User.objects.filter(id=patient.user.id).first()
        if patient:
            is_edit_mode = True 
    if request.method == 'POST':
        doctForm = PatientForm(request.POST, instance=patient)
        userForm = UserForm(request.POST, instance=userInfo)
        if is_edit_mode:
            userForm = UserChangeForm(request.POST,instance=userInfo)
        if doctForm.is_valid() and userForm.is_valid():
            user = userForm.save(commit=False)
            if not is_edit_mode: 
                user.is_staff = False
                user.username = get_unique_user_id()
            user.save()
            patient = doctForm.save(commit=False)
            patient.user = user
            patient.save()
            doctForm.save_m2m()
            return redirect('patient_mng')
    else:
        doctForm = PatientForm(instance=patient)
        userForm = UserForm(instance=userInfo)

    return render(request, 'patient_form.html', {'patientForm': doctForm, 'userForm': userForm,'patients':patients,'is_edit_mode':is_edit_mode})

@login_required
@permission_required('auth', raise_exception=True)
def delete_patient(request):
    id = request.POST.get('user')
    if not request.user.is_superuser:
        raise PermissionDenied
    user = get_object_or_404(User, id=id)
    user.delete()
    return redirect(reversed('patient_mng'))

@login_required
@permission_required('auth', raise_exception=True)
def manage_appointments(request):
    form = AppointmentForm()
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Appointment created")
    appointments = Appointment.objects.all().exclude(status='completed')
    return render(request,'appointment_manage.html',{'appointments':appointments,'form':form})

@login_required
@permission_required('auth', raise_exception=True)
def delete_appointment(request,app_id):
    appointment = Appointment.objects.filter(id=app_id).filter()
    if appointment:
        appointment.delete()
        messages.success(request,"Appointment Deleted successfully")
    return redirect('manage_appointments')

@login_required
@permission_required('auth', raise_exception=True)
def accept_appointment(request,app_id):
    appointment = Appointment.objects.filter(id=app_id).filter()
    if appointment:
        appointment.update(status='confirmed')
        messages.success(request,"Appointment confirmed successfully")
    return redirect('manage_appointments')

@login_required
@permission_required('auth', raise_exception=True)
def complete_appointment(request,app_id):
    appointment = Appointment.objects.filter(id=app_id).filter()
    if appointment:
        appointment.update(status='completed')
        messages.success(request,"Appointment confirmed successfully")
    return redirect('manage_appointments')

@login_required
@permission_required('auth', raise_exception=True)
def manage_bills(request,app_id=None):
    prescriptions = Prescription.objects.filter(appointment__status='completed').exclude(appointment__bill__isnull=False)
    appointment = Appointment.objects.filter(id=app_id).filter()
    if appointment:
        form = BillForm()
        if request.method == 'POST':
            form = BillForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'Payment successful')
                return render(request,'bills.html',{'prescriptions':prescriptions})
        return render(request,'bills.html',{'prescriptions':prescriptions,'form':form,'app_id':app_id})
    return render(request,'bills.html',{'prescriptions':prescriptions})

@login_required
@permission_required('auth', raise_exception=True)
def manage_post(request, post_id=None):
    posts = DentalPost.objects.all().order_by('-id')
    post_instance = None
    editable = False
    if post_id:
        post_instance = get_object_or_404(DentalPost, id=post_id)
        editable = True
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES,instance=post_instance)
        if form.is_valid():
            post_save = form.save(commit=False)
            if not post_save.pk: 
                post_save.user = request.user
            post_save.save()
            return redirect('post_index')  
    else:
        form = PostForm(instance=post_instance)
    return render(request, 'manage_post.html', {'form': form,'posts':posts,'editable':editable})

def post_delete(request,post_id):
    post = get_object_or_404(DentalPost, id=post_id)
    post.delete()
    messages.success(request,"Post deleted successfully")
    return redirect('post_index')