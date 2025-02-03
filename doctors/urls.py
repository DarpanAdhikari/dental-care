from django.urls import path
from . import views

urlpatterns = [
    path('',views.doctors_info,name='doctors_index'),
    path('appointment/',views.view_appointment,name='doctors_appointment'),
    path('appointment/<int:app_id>/confirm',views.confirm_appointment,name='confirm_appointment'),
    path('appointment/<int:app_id>/cancel',views.cancel_appointment,name='cancel_appointment'),
    path('prescriptions/',views.manage_prescription,name='manage_prescription'),
    path('prescriptions/<int:app_id>/prescribe',views.manage_prescription,name='prescription_form'),
    path('edit_profile/',views.edit_profile,name='edit_profile')
]
