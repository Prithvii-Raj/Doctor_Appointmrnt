from django import forms
from django.contrib.auth.models import User

ROLE_CHOICES = [
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
]

class SignupForm(forms.ModelForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {'username':None}
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES)

class OTPForm(forms.Form):
    email = forms.EmailField(widget=forms.HiddenInput())
    otp = forms.CharField(max_length=6, label="Enter OTP")
