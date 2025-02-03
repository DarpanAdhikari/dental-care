from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.patient_register, name='register_patient'),
    path('dashboard/',views.patient_details,name='pat_dashboard'),
    path('dashboard/<int:presc_id>/view/',views.patient_details,name='view_prescription'),
    path('edit_patient_info/<int:user_id>/',views.edit_patient_profile,name='edit_profile'),
    path('dashboard/<int:presc_id>/<int:bill_id>/',views.verify_payment,name='payment_verification')
]
