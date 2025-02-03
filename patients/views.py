from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from accounts.models import Patient,Doctor
from django.contrib.auth.models import User
from django.contrib.auth import login
from accounts.views import redirectUser
from doctors.models import *
from .form import *
from accounts.form import UserForm
from django.contrib import messages
import random
from django.db.models import Q
import hashlib,uuid,hmac,base64,json

def generate_random_number():
    part1 = str(random.randint(0, 9999)).zfill(4)
    part2 = str(random.randint(0, 9999)).zfill(4)
    return f"{part1}-{part2}"

def get_unique_user_id():
    while True:
        user_id = generate_random_number()
        if not User.objects.filter(username=user_id).exists():
            return user_id

def not_staff_or_superuser_check(user):
    return not user.is_staff and not user.is_superuser

@login_required
@user_passes_test(not_staff_or_superuser_check, login_url='/accounts/login/')
def patient_details(request, presc_id=None):
    getPatientData = Patient.objects.filter(user=request.user).first()
    notification = Notification.objects.filter(user=request.user)
    appointment = Appointment.objects.filter(Q(patient=getPatientData.id) & (Q(status='pending') | Q(status='confirmed')))
    prescriptions = Appointment.objects.filter(Q(patient=getPatientData.id) & (Q(status='completed')))
    prescription = None
    if presc_id:
        prescription = Prescription.objects.filter(
                appointment__id=presc_id,
                appointment__bill__isnull=False, 
                appointment__bill__payment_status=True 
            ).first()

        if not prescription:
            bill = Bill.objects.filter(appointment__id=presc_id).first()
            if bill:
                pay = pay_medical_bill(bill.amount, presc_id,bill.id)
                if pay:
                    return render(request,'patient_info.html',{'userData':getPatientData,'notifications':notification,\
                    'appointments':appointment,'prescriptions':prescriptions,'pay':pay})
            else:
                messages.error(request,"Bill is not prepared yet please wait!")
                return redirect('pat_dashboard')
    return render(request,'patient_info.html',{'userData':getPatientData,'notifications':notification,\
         'appointments':appointment,'prescriptions':prescriptions,'prescription':prescription})

def patient_register(request):
    if request.user.is_authenticated:
        return redirectUser(request.user)
    if request.method == 'POST':
        patientForm = PatientForm(request.POST)
        userForm = UserForm(request.POST) 
        if patientForm.is_valid() and userForm.is_valid():
            user = userForm.save(commit=False)
            user.is_staff = False
            user.username = get_unique_user_id()
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.save()
            login(request, user)
            return redirect('home')
    else:
        patientForm = PatientForm()
        userForm = UserForm()
    
    return render(request, 'patient_register.html', {'patientForm': patientForm, 'userForm': userForm})

@login_required
@user_passes_test(not_staff_or_superuser_check, login_url='/accounts/login/')
def edit_patient_profile(request, user_id):
    patient = Patient.objects.filter(user=user_id).first()
    userInfo = User.objects.filter(id=patient.user.id).first()
    if not patient:
        return redirect('home')
    if request.method == 'POST':
        patientForm = PatientForm(request.POST, instance=patient) 
        if patientForm.is_valid() and userForm.is_valid():
            user = userForm.save(commit=False)
            user.is_staff = False
            user.username = get_unique_user_id()
            user.save()
            patient = patientForm.save(commit=False)
            patient.user = user
            patient.save()
            login(request, user)
            return redirect('home')
    else:
        patientForm = PatientForm(instance=patient)
        userForm = UserForm(instance=userInfo) 
    return render(request, 'edit_profile_info.html', {'patientForm': patientForm, 'userForm': userForm})

def genSha256(key, message):
    key = key.encode('utf-8')
    message = message.encode('utf-8')
    hmac_sha256 = hmac.new(key, message, hashlib.sha256)
    digest = hmac_sha256.digest()
    signature = base64.b64encode(digest).decode('utf-8')
    return signature
def pay_medical_bill(amount, presc_id,bill_id):
    SECRET_KEY = "8gBm/:&EnhH.1/q"
    transaction_uuid = str(uuid.uuid4())
    product_code = "EPAYTEST"
    amount = int(amount)
    taxAmount = 0
    total_amount = amount + taxAmount
    data_to_sign = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    payUrl = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
    data = {
        "amount": str(amount),
        "tax_amount": str(taxAmount),
        "total_amount": str(total_amount),
        "transaction_uuid": transaction_uuid,
        "product_code": product_code,
        "product_service_charge": 0,
        "product_delivery_charge": 0,
        "success_url": f"http://localhost:8000/patient/dashboard/{presc_id}/{bill_id}/",
        "failure_url": f"http://localhost:8000/patient/dashboard/",
        "signed_field_names": "total_amount,transaction_uuid,product_code",
        "signature": genSha256(SECRET_KEY, data_to_sign),
    }
    return {'payUrl': payUrl, 'data': data}


def verify_payment(request,presc_id,bill_id):
    data = request.GET.get('data')
    decoded_bytes = base64.b64decode(data)
    decoded_string = decoded_bytes.decode('utf-8')
    decoded_json = json.loads(decoded_string)
    try:
        decoded_json = json.loads(decoded_string)
        transaction_code = decoded_json.get('transaction_code')
        bill = get_object_or_404(Bill, id=bill_id)
        bill.payment_status = True
        bill.invoice_num = transaction_code
        bill.save()
        messages.success(request,"Payment success")
        return redirect('view_prescription', presc_id=presc_id)
    except (json.JSONDecodeError, TypeError) as e:
        print("Error decoding JSON or invalid data:", e)
    return redirect('pat_dashboard')