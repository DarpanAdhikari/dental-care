from django.urls import path
from . import views

urlpatterns = [
    path('',views.admin_index,name='admin_index'),
    path('doctor/',views.doctor_form,name='doctor_mng'),
    path('doctor/<int:user_id>/',views.doctor_form, name='edit_doctor'),
    path('doctor/delete/',views.delete_doctor, name='delete_doctor'),
    path('patient/',views.patient_form,name='patient_mng'),
    path('patient/<int:user_id>/',views.patient_form,name='edit_patient'),
    path('patient/delete/',views.delete_patient,name='delete_patient'),
    path('appointments/',views.manage_appointments,name='manage_appointments'),
    path('appointments/<int:app_id>/confirm/',views.accept_appointment, name='accept_appointment'),
    path('appointments/<int:app_id>/complete/',views.complete_appointment, name='complete_appointment'),
    path('appointments/<int:app_id>/delete/',views.delete_appointment,name='delete_appointment'),
    path('bills/',views.manage_bills,name='bills'),
    path('bills/<int:app_id>/pay',views.manage_bills,name='bill_pay'),
    path('manage_post/',views.manage_post, name='post_index'),
    path('manage_post/<int:post_id>/edit/',views.manage_post, name='post_edit'),
    path('manage_post/<int:post_id>/delete/',views.post_delete, name='post_delete')
]
