from django.urls import path
from .views import dashpatient_view, docpatient_view, patient_view, change_doctor, edit_patient_profile

urlpatterns = [
    path('patientdashboard/', dashpatient_view, name='patientdashboard'),
    path('listofdoct/', docpatient_view, name= 'listofdoct'),
    path('patient/', patient_view, name='patient'),
    path('changedoctor/', change_doctor, name='changedoctor'),
    path('editpatientprofile/', edit_patient_profile, name='editpatientprofile'),
    
]