# forms.py in useradmin app
from django import forms
from django.contrib.auth import get_user_model

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'role']
    
    # Add custom validation or field widgets as necessary
