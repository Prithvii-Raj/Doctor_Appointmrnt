# authapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .forms import SignupForm, LoginForm, OTPForm
from accounts.models import DoctorProfile, PatientProfile

# For OTP
import random
from email_validator import validate_email, EmailNotValidError  # UPDATED

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

#Added extra
def landing(request):
    return render(request, 'authapp/landing.html')

def services(request):
    return render(request, 'authapp/services.html')

def about(request):
    return render(request, 'authapp/about.html')

def contact(request):
    return render(request, 'authapp/contact.html')
#End here

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data['email']

            # Validate email using email-validator
            try:
                validated_email = validate_email(email, check_deliverability=True)
                email = validated_email.email  # Get normalized email
            except EmailNotValidError as e:
                form.add_error(None, f"Invalid Email: {str(e)}")
                return render(request, 'authapp/signup.html', {'form': form})

            # Generate OTP
            otp = str(random.randint(100000, 999999))

            # Save OTP and user form data temporarily in session
            request.session['otp'] = otp
            request.session['user_data'] = form.cleaned_data

            try:
                # Send OTP to email
                send_mail(
                    subject='Your Signup OTP',
                    message=f'Your OTP for signup is {otp}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                )
            except Exception:
                form.add_error(None, "Failed to send email. Please check your SMTP settings.")
                return render(request, 'authapp/signup.html', {'form': form})

            return redirect('verify_otp')

    else:
        form = SignupForm()

    return render(request, 'authapp/signup.html', {'form': form})


def verify_otp_view(request):
    otp_session = request.session.get('otp')
    user_data = request.session.get('user_data')

    if not otp_session or not user_data:
        return redirect('signup')  # If refreshed without signup

    form = OTPForm(initial={'email': user_data['email']})

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if entered_otp == otp_session:

                # Create user after OTP verified
                user = User(
                    username=user_data['username'],
                    email=user_data['email']
                )
                user.set_password(user_data['password'])
                user.save()

                role = user_data['role']
                group, _ = Group.objects.get_or_create(name=role.capitalize())
                user.groups.add(group)

                if role == 'doctor':
                    DoctorProfile.objects.create(user=user)
                elif role == 'patient':
                    PatientProfile.objects.create(user=user)

                del request.session['otp']
                del request.session['user_data']

                return redirect('login')
            else:
                return render(request, 'authapp/verify_otp.html', {'form': form, 'error': 'Invalid OTP!'})

    return render(request, 'authapp/verify_otp.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            user = authenticate(request, username=username, password=password)

            if user:
                if user.groups.filter(name=role.capitalize()).exists():
                    login(request, user)
                    return redirect('doctor_dashboard' if role == 'doctor' else 'patient_dashboard')
                else:
                    form.add_error(None, 'Incorrect role for this account.')
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'authapp/login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')
