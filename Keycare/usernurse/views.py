from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test 
from accounts.models import CustomUser, PatientProfile
from django.db.models import Q
from django.views.decorators.cache import never_cache


def is_nurse(user):
    return user.role == 'Nurse'

@login_required
@never_cache
@user_passes_test(is_nurse)
def dashnurse_view(request):
    if 'username' in request.session:
        del request.session['username']

    count = {
        'patient_count': CustomUser.objects.filter(role='Patient').count()
    }
    patients = CustomUser.objects.filter(role='Patient')
    patients_doctors = []
    for patient in patients:
    
        patient_profile = PatientProfile.objects.get(user=patient)
        doctor = patient_profile.assigned_doc
        patients_doctors.append({
            'patient': patient,
            'doctor': doctor
        })

    return render(request, 'dashnurse.html', {'count': count, 'patients_doctors': patients_doctors})

@login_required
@never_cache
@user_passes_test(is_nurse)
def patientnurse_view(request):
    query = request.GET.get('q', '').strip()

    # Get all patients
    patients = CustomUser.objects.filter(role='Patient')

    if query:
        # Filter patients by first name, last name, or assigned doctor's name
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(patientprofile__assigned_doc__user__first_name__icontains=query) |
            Q(patientprofile__assigned_doc__user__last_name__icontains=query)
        ).distinct()

    patients_doctors = []
    for patient in patients:
        try:
            patient_profile = PatientProfile.objects.get(user=patient)
            doctor = patient_profile.assigned_doc
            patients_doctors.append({
                'patient': patient,
                'doctor': doctor
            })
        except PatientProfile.DoesNotExist:
            continue

    context = {
        'patients_doctors': patients_doctors,
        'query': query,
    }

    return render(request, 'patientnurse.html', context)

@login_required
@user_passes_test(is_nurse, login_url='login')
def patientview_view(request,pk):
    patients = get_object_or_404(PatientProfile, user_id=pk)
    assignedoc = patients.assigned_doc.user.first_name + ' ' + patients.assigned_doc.user.last_name

    context = {
        'patient': patients,
        'assignedoc': assignedoc
        }

    return render(request, 'patientsview.html', context)
