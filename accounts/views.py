from django.shortcuts import render,redirect
from .models import Appointment,DoctorProfile,PatientProfile
from .forms import DoctorProfileForm,PatientProfileForm

# For email notification
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User   # Not required

# example views
from django.contrib.auth.decorators import login_required, user_passes_test

def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()

def is_patient(user):
    return user.groups.filter(name='Patient').exists()


# Doctor Dashboard
@login_required
@user_passes_test(is_doctor)
def doctor_dashboard(request):
    return render(request, 'accounts/doctor_dashboard.html')

# Patient Dashboard
@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):

    # Get the logged-in patient's profile and appoitments
    patient = request.user.patientprofile
    appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')
    context = {
        'patient': patient,
        'appointments': appointments
    }
    
    return render(request, 'accounts/patient_dashboard.html',context)


from .forms import AppointmentForm
# Appoitment Booking
@login_required
@user_passes_test(is_patient)
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patientprofile
            appointment.status = 'Pending'
            appointment.save()

            # send vonfirmation email to the patient

            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'accounts/book_appointment.html', {'form': form})


# All appointments
@login_required
@user_passes_test(is_doctor)
def manage_appointments(request):
    doctor = request.user.doctorprofile
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'accounts/manage_appointments.html', {'appointments': appointments})


from django.shortcuts import get_object_or_404
# Confirm appointment
@login_required
@user_passes_test(is_doctor)
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctorprofile)
    appointment.status = 'Confirmed'
    appointment.save()

    # Send confirmation email
    send_mail(
        subject='Appointment Confirmed',
        message=f'Hi {appointment.patient.user.username}, your appointment with Dr. {appointment.doctor.user.username} on {appointment.date} has been confirmed.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[appointment.patient.user.email],
        fail_silently=True,
    )

    return redirect('manage_appointments')

# cancel appoitment
@login_required
@user_passes_test(is_patient)
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patientprofile)
    
    # Only allow cancel if it's still pending or confirmed
    if appointment.status in ['Pending', 'Confirmed']:
        appointment.status = 'Cancelled'
        appointment.save()

        # Send cancellation email
        send_mail(
            subject='Appointment Cancelled',
            message=f'Hi {appointment.patient.user.username}, your appointment with Dr. {appointment.doctor.user.username} on {appointment.date} has been cancelled.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[appointment.patient.user.email],
            fail_silently=True,
        )

    return redirect('patient_dashboard')

# Doctor Profile Edit
@login_required
@user_passes_test(is_doctor)
def edit_doctor_profile(request):
    doctor = request.user.doctorprofile
    if request.method == 'POST':
        profile_form = DoctorProfileForm(request.POST, instance=doctor)
        if  profile_form.is_valid():
            profile_form.save()
            return redirect('doctor_dashboard')
    else:
        profile_form = DoctorProfileForm(instance=doctor)
    return render(request, 'accounts/edit_doctor_profile.html', {'profile_form': profile_form})


# Patient Profile Edit
@login_required
@user_passes_test(is_patient)
def edit_patient_profile(request):
    patient = request.user.patientprofile
    if request.method == 'POST':
        profile_form = PatientProfileForm(request.POST, instance=patient)
        if  profile_form.is_valid():
            profile_form.save()
            return redirect('patient_dashboard')
    else:
        profile_form = PatientProfileForm(instance=patient)
    return render(request, 'accounts/edit_patient_profile.html', {'profile_form': profile_form})


# For downloading csv file of patients
import csv
from django.http import HttpResponse

@login_required
@user_passes_test(is_doctor)
def download_patient_list(request):
    doctor = request.user.doctorprofile
    appointments = Appointment.objects.filter(doctor=doctor)

    # Create the HTTP response with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="patient_list.csv"'

    writer = csv.writer(response)
    writer.writerow(['Patient Name', 'Email', 'Age', 'Gender', 'Appointment Date', 'Status'])

    for appt in appointments:
        writer.writerow([
            appt.patient.user.username,
            appt.patient.user.email,
            appt.patient.age,
            appt.patient.gender,
            appt.date,
            appt.status,
        ])

    return response

# Greatings
from datetime import datetime

@login_required
@user_passes_test(is_patient)
def patient_dashboard(request):
    patient = request.user.patientprofile
    appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')
    
    # Get current hour
    current_hour = datetime.now().hour
    
    # Determine greeting
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= current_hour < 21:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"

    context = {
        'patient': patient,
        'appointments': appointments,
        'greeting': greeting
    }
    
    return render(request, 'accounts/patient_dashboard.html', context)