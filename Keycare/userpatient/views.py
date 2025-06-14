from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test 
from accounts.models import CustomUser, PatientProfile, DoctorProfile
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from useradmin.forms import CustomUserForm, PatientProfileForm
from django.db.models import Q
from django.views.decorators.cache import never_cache



def is_patient(user):
    return user.role == 'Patient'

@login_required
@never_cache
@user_passes_test(is_patient)
def dashpatient_view(request):
    
    try:
        # Get the PatientProfile for the logged-in user
        patient_profile = PatientProfile.objects.get(user=request.user)
        patient_profiles = PatientProfile.objects.filter(user=request.user)

        # Check if assigned_doc is set (not None)
        if patient_profile.assigned_doc:
            assigned_doctor = patient_profile.assigned_doc
            assigned_doctor_name = assigned_doctor.user.first_name + ' ' + assigned_doctor.user.last_name  # Get doctor's name from related CustomUser
            assigned_doctor_department = assigned_doctor.departement  # Get the doctor's department
        else:
            assigned_doctor_name = None
            assigned_doctor_department = None

    except PatientProfile.DoesNotExist:
        # If no PatientProfile exists for the logged-in user
        patient_profile = None
        assigned_doctor_name = None
        assigned_doctor_department = None

    context = {
        'patient_profile': patient_profiles,
        'assigned_doctor_name': assigned_doctor_name,
        'assigned_doctor_department': assigned_doctor_department,
    }
    return render(request, 'dashpatient.html', context)

@login_required
@never_cache
@user_passes_test(is_patient)
def docpatient_view(request):
    query = request.GET.get('q', '').strip()
    doctors = CustomUser.objects.filter(role='Doctor')

    if query:
        doctors = doctors.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(doctorprofile__departement__icontains=query)
        ).distinct()

    doctor_info = []
    for doctor in doctors:
        try:
            doctor_profile = DoctorProfile.objects.get(user=doctor)
            doctor_info.append({
                'doctor': doctor,
                'department': doctor_profile.departement,
                'doctor_id': doctor_profile.id
            })
        except DoctorProfile.DoesNotExist:
            doctor_info.append({
                'doctor': doctor,
                'department': None,
                'doctor_id': None
            })

    context = {
        'doctor_info': doctor_info,
        'query': query,
    }

    return render(request, 'docpatient.html', context)

@login_required
@user_passes_test(is_patient)
def patient_view(request):
    try:
        patient_profile = PatientProfile.objects.get(user=request.user)  
    except PatientProfile.DoesNotExist:
        patient_profile = None  

    return render(request, 'patient.html', {'patient_profile': patient_profile})  

@login_required
@user_passes_test(is_patient)
def change_doctor(request):
    if request.method == 'POST':
        try:
            patient_profile = PatientProfile.objects.get(user=request.user)
            new_doctor_id = request.POST.get('doctor')  # Get the doctor ID from the form

            if not new_doctor_id:
                messages.error(request, 'No doctor selected.')
                return redirect('listofdoct')  

            new_doctor = DoctorProfile.objects.get(id=new_doctor_id)

            if patient_profile.assigned_doc == new_doctor:
                messages.info(request, 'You are already assigned to this doctor.')
                return redirect('listofdoct')  

            patient_profile.assigned_doc = new_doctor
            patient_profile.save()

            messages.success(request, f'Your doctor has been changed to Dr. {new_doctor.user.first_name} {new_doctor.user.last_name}')
            return redirect('patientdashboard')  

        except PatientProfile.DoesNotExist:
            messages.error(request, 'Patient profile not found.')
            return HttpResponse("Patient profile not found", status=404)
        except DoctorProfile.DoesNotExist:
            messages.error(request, 'Selected doctor does not exist.')
            return HttpResponse("Doctor not found", status=404)

    else:
        doctors = DoctorProfile.objects.all()
        return render(request, 'docpatient.html', {'doctor_info': doctors})
    
@login_required
@user_passes_test(is_patient)
def edit_patient_profile(request):
    patient_profile = get_object_or_404(PatientProfile, user=request.user)
    user = request.user 

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        profile_form = PatientProfileForm(request.POST, instance=patient_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save the user (CustomUser)
            profile_form.save()  # Save the patient profile
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('patientdashboard')
    else:
        user_form = CustomUserForm(instance=user)
        profile_form = PatientProfileForm(instance=patient_profile)

    return render(request, 'edit_patient_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'patient_profile': patient_profile
    })