from django import forms
from .models import Appointment, DoctorProfile,PatientProfile

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }



# Profile for Doctor and patient
class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'experience']


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['age', 'gender']