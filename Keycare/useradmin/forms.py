# forms.py in useradmin app
from django import forms
from django.contrib.auth import get_user_model
from  accounts.models import DoctorProfile, NurseProfile, CustomUser, PatientProfile



class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'role']

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['departement']

class NurseProfileForm(forms.ModelForm):
    class Meta:
        model = NurseProfile
        fields = ['expertise']

# User form for patient edit
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

# Patient profile form for patient edit.
class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['age', 'weight', 'height', 'blood_type', 'gender']

# Doctor patient edit form.
class DoctorPatientEdit(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['dieases', 'symptomps', 'notes']



