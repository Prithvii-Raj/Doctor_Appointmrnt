from django.db import models
# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.patient.user.username} → {self.doctor.user.username} on {self.date}"


