from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class CustomUser (AbstractUser):
    activity_log = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=20, choices= (('Admin', 'Admin'),('Doctor', 'Doctor'), ('Nurse', 'Nurse'), ('Patient', 'Patient')), blank=True)

    def __str__(self):
        return self.username

class DoctorProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=000)
    departement = models.CharField(max_length=20)

    def __str__(self):
        return f'Doctor Profile for {self.user.username}'
    
class NurseProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=000)
    expertise = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f'Nurse Profile for {self.user.username}'

class PatientProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=000)
    age = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    blood_type = models.CharField(max_length=3, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),('O+', 'O+'), ('O-', 'O-'),('AB+', 'AB+'), ('AB-', 'AB-')], null=True, blank=True)
    gender = models.CharField(max_length=10, choices= (('male', 'Male'), ('female', 'Female')), blank=True)
    assigned_doc = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    dieases = models.TextField(null=True, blank=True)
    symptomps = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)


    def __str__(self):
        return f'Patient Profile for {self.user.username}'