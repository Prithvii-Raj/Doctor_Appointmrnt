from django.urls import path
from . import views

urlpatterns = [
    
    # dashboard routes
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),

    path('book/', views.book_appointment, name='book_appointment'),
    path('manage/', views.manage_appointments, name='manage_appointments'),
    path('confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_appointment'),


    path('doctor/edit-profile/', views.edit_doctor_profile, name='edit_doctor_profile'),
    path('patient/edit-profile/', views.edit_patient_profile, name='edit_patient_profile'),

    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

    # for csv file of patients
    path('download_patient_list/', views.download_patient_list, name='download_patient_list'),


]