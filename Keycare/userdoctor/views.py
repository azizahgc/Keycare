from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import CustomUser, PatientProfile, DoctorProfile
from useradmin.forms import DoctorPatientEdit
from django.db.models import Q
from django.views.decorators.cache import never_cache


def is_doctor(user):
    return user.role == 'Doctor'

@login_required
@never_cache
@user_passes_test(is_doctor)
def dashdoc_view(request):
    if 'username' in request.session:
        del request.session['username']

    count = {
        'patient_count': CustomUser.objects.filter(role='Patient').count()
    }
    print("Patient Count:", count['patient_count'])

    patients = CustomUser.objects.filter(role='Patient')
    doctor = CustomUser.objects.get(username=request.user)
    assignedoc = DoctorProfile.objects.get(user_id=doctor.id)

    patients = CustomUser.objects.filter(role='Patient', patientprofile__assigned_doc=assignedoc.id)


    patient_info = []
    for patient in patients:
        try:
            patient_profile = PatientProfile.objects.get(user=patient, assigned_doc=assignedoc.id)
            patient_info.append({
                'patient' : patient,
                'dieases' : patient_profile.dieases,
                'patient_id' : patient_profile.id
            })
        except PatientProfile.DoesNotExist:
            patient_info.append({
                'patient': None,
                'dieases': None,
                'patient_id' : None
            })

    return render(request, 'dashdoctor.html', {'count': count, 'patient_info': patient_info})

@login_required
@never_cache
@user_passes_test(is_doctor)
def patientdoc_view(request):
    query = request.GET.get('q', '').strip()

    doctor_user = request.user
    assignedoc = DoctorProfile.objects.get(user=doctor_user)

    patients = CustomUser.objects.filter(role='Patient', patientprofile__assigned_doc=assignedoc.id)

    if query:
        patients = patients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(patientprofile__dieases__icontains=query)
        ).distinct()

    patient_info = []
    for patient in patients:
        try:
            patient_profile = PatientProfile.objects.get(user=patient, assigned_doc=assignedoc.id)
            patient_info.append({
                'patient': patient,
                'dieases': patient_profile.dieases,
                'patient_id': patient_profile.id
            })
        except PatientProfile.DoesNotExist:
            continue

    context = {
        'patient_info': patient_info,
        'query': query,
    }

    return render(request, 'patientdoc.html', context)

@login_required
@user_passes_test(is_doctor)
def docpatientprofile_view(request, pk):
    doctor = CustomUser.objects.get(username=request.user)
    assignedoc = DoctorProfile.objects.get(user_id=doctor.id)

    patient_profile = get_object_or_404(PatientProfile, user_id=pk, assigned_doc=assignedoc)

    if request.method == 'POST':
        form = DoctorPatientEdit(request.POST, instance=patient_profile)
        if form.is_valid():
            form.save()
            return redirect('patientdoc')
    else:
        form = DoctorPatientEdit(instance=patient_profile)

    return render(request, 'doctor.html', {'form': form, 'patient_profile': patient_profile})


