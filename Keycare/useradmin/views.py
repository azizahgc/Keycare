from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.models import CustomUser, DoctorProfile, NurseProfile, PatientProfile
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from .forms import UserRegistrationForm, DoctorProfileForm, NurseProfileForm
from django.contrib.auth import get_user_model
from django.db.models import Q 
from django.contrib import messages
import calendar
from django.views.decorators.cache import never_cache




def is_admin(user):
    return user.role == 'Admin'

@login_required
@never_cache
@user_passes_test(is_admin, login_url='login')  # Redirect to login if not an admin
def dashboard_view(request):
    if 'username' in request.session:
        del request.session['username']
    
    # Get counts for each group using your custom user model
    count = {
        'doctor_count': CustomUser.objects.filter(role='Doctor').count(),
        'nurse_count': CustomUser.objects.filter(role='Nurse').count(),
        'patient_count': CustomUser.objects.filter(role='Patient').count(),
    }
    print("Doctor Count:", count['doctor_count'])

    # Get all CustomUsers and the latest activity logs
    users = CustomUser.objects.all()
    activity_logs = CustomUser.objects.all().order_by('-last_login')[:5]
    print(count)  # To verify counts are correct

    # Return the rendered template with the count data
    return render(request, 'dashadmin.html', {'count': count, 'users': users, 'activity_log': activity_logs})

@login_required
@never_cache
@user_passes_test(is_admin, login_url='login')
def listofdoc_view(request):
    doctors = CustomUser.objects.filter(role='Doctor')

    doctor_info = []
    for doctor in doctors:
        try:
            # Query DoctorProfile directly using the user foreign key
            doctor_profile = DoctorProfile.objects.get(user=doctor)
            doctor_info.append({
                'doctor': doctor,
                'department': doctor_profile.departement
            })
        except DoctorProfile.DoesNotExist:
            doctor_info.append({
                'doctor': doctor,
                'department': None  # If doctor does not have a profile, set department to None
            })
    return render(request, 'docadmin.html', {'doctor_info': doctor_info})


@login_required
@user_passes_test(is_admin, login_url='login')
def listofdoctor_view(request, pk):
    doctors = CustomUser.objects.filter(role='Doctor')

    doctor_info = []
    for doctor in doctors:
        try:
            # Query DoctorProfile directly using the user foreign key
            doctor_profile = DoctorProfile.objects.get(user=doctor)
            doctor_info.append({
                'doctor': doctor,
                'department': doctor_profile.departement
            })
        except DoctorProfile.DoesNotExist:
            doctor_info.append({
                'doctor': doctor,
                'department': None  # If doctor does not have a profile, set department to None
            })
    return render(request, 'docadmin.html', {'doctor_info': doctor_info})

@login_required
@never_cache
@user_passes_test(is_admin, login_url='login')
def nurseadmin_view(request):
    nurses = CustomUser.objects.filter(role='Nurse')
    
    nurse_info = []
    for nurse in nurses:
        try:
            # Query NurseProfile directly using the user foreign key
            nurse_profile = NurseProfile.objects.get(user=nurse)
            nurse_info.append({
                'nurse': nurse,
                'expertise': nurse_profile.expertise
            })
        except NurseProfile.DoesNotExist:
            nurse_info.append({
                'nurse': nurse,
                'expertise': None  # If nurse does not have a profile, set expertise to None
            })
    return render(request, 'nurseadmin.html', {'nurse_info': nurse_info})

@login_required
@user_passes_test(is_admin, login_url='login')
def nurseadmin2_view(request, pk):
    nurses = CustomUser.objects.filter(role='Nurse')

    nurse_info = []
    for nurse in nurses:
        try:
            # Query NurseProfile directly using the user foreign key
            nurse_profile = NurseProfile.objects.get(user=nurse)
            nurse_info.append({
                'nurse': nurse,
                'expertise': nurse_profile.expertise
            })
        except NurseProfile.DoesNotExist:
            nurse_info.append({
                'nurse': nurse,
                'expertise': None  # If nurse does not have a profile, set expertise to None
            })
    return render(request, 'nurseadmin.html', {'nurse_info': nurse_info})

@login_required
@never_cache
@user_passes_test(is_admin, login_url='login')
def patientadmin_view(request):
    # Optimize with select_related to reduce database queries
    patients = CustomUser.objects.filter(role='Patient').select_related()

    patient_info = []
    for patient in patients:
        try:
            patient_profile = PatientProfile.objects.select_related('assigned_doc__user').get(user=patient)
            
            # Get assigned doctor info safely
            assigned_doc = None
            if patient_profile.assigned_doc and patient_profile.assigned_doc.user:
                doc_first = patient_profile.assigned_doc.user.first_name or ""
                doc_last = patient_profile.assigned_doc.user.last_name or ""
                assigned_doc = f"{doc_first} {doc_last}".strip()
                if not assigned_doc:  # If both names are empty
                    assigned_doc = "Unnamed Doctor"
            
            # Create a single dictionary entry for each patient
            patient_info.append({
                'patient': patient,
                'age': patient_profile.age,
                'weight': patient_profile.weight,
                'height': patient_profile.height,
                'blood_type': patient_profile.blood_type,
                'gender': patient_profile.gender,
                'dieases': patient_profile.dieases,
                'symptomps': patient_profile.symptomps,
                'assigned_doc': assigned_doc
            })

        except PatientProfile.DoesNotExist:
            # Create a single dictionary entry for patients without profiles
            patient_info.append({
                'patient': patient,
                'age': None,
                'weight': None,
                'height': None,
                'blood_type': None,
                'gender': None,
                'dieases': None,
                'symptomps': None,
                'assigned_doc': None
            })
    
    return render(request, 'patientadmin.html', {'patient_info': patient_info})

@login_required
@user_passes_test(is_admin, login_url='login')
def patientadmin2_view(request,pk):
    patients = get_object_or_404(PatientProfile, user_id=pk)
    assignedoc = patients.assigned_doc.user.first_name + ' ' + patients.assigned_doc.user.last_name

    context = {
        'patient': patients,
        'assignedoc': assignedoc
        }

    return render(request, 'patients.html', context)


@login_required
@never_cache
@user_passes_test(is_admin, login_url='login')
def logactadmin_view(request):
    activity_logs = CustomUser.objects.all().order_by('-last_login')[:10]
    return render(request, 'logactadmin.html', { 'activity_log': activity_logs})


def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")


@login_required
@user_passes_test(is_admin)
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')  
        last_name = request.POST.get('last_name')
        departement = request.POST.get('departement')
        expertise = request.POST.get('expertise')
        age = request.POST.get('age')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        blood_type = request.POST.get('blood_type')
        gender = request.POST.get('gender')
        dieases = request.POST.get('dieases')
        symptomps = request.POST.get('symptomps')

        try:
            # Validate password before creating user
            validate_password(password)
            hashed_password = make_password(password)

            user = get_user_model().objects.create(
                username=username,
                email=email,
                password=hashed_password,
                first_name=first_name,
                last_name=last_name,
                role='Doctor' if 'doctor' in request.path else 'Nurse' if 'nurse' in request.path else 'Patient'
            )
            
            if 'doctor' in request.path:
                departement = request.POST.get('departement')
                DoctorProfile.objects.create(user=user, departement=departement)
                return render(request, 'registdoc.html', {'success': 'Doctor created successfully!'})  

            elif 'nurse' in request.path:
                expertise = request.POST.get('expertise')
                NurseProfile.objects.create(user=user, expertise=expertise)
                return render(request, 'registnurse.html', {'success': 'Nurse created successfully!'})  

            elif 'patient' in request.path:
                doctors = DoctorProfile.objects.all()
                age = request.POST.get('age')
                weight = request.POST.get('weight')
                height = request.POST.get('height')
                blood_type = request.POST.get('blood_type')
                gender = request.POST.get('gender')
                dieases = request.POST.get('dieases')
                symptomps = request.POST.get('symptomps')
                assigned_doc_id = request.POST.get('assigned_doc')  

                assigned_doc = DoctorProfile.objects.get(id=assigned_doc_id) if assigned_doc_id else None

                PatientProfile.objects.create(
                    user=user,
                    age=age,
                    weight=weight,
                    height=height,
                    blood_type=blood_type,
                    gender=gender,
                    dieases=dieases,
                    symptomps=symptomps,
                    assigned_doc=assigned_doc
                )
                return render(request, 'registpatient.html', {'success': 'Patient created successfully!', 'doctors': doctors})  

            return redirect('dashboard')  

        except ValidationError as e:
            # Handle password validation errors - KEEP THE FORM DATA
            print(f"Validation error: {e.messages}")  # Debug print
            error_message = e.messages[0] if e.messages else 'Password validation failed'
            
            # Create context with error message and preserve form data
            context = {
                'error': error_message,
                'request': request  # Pass request object to template
            }
            
            if 'doctor' in request.path:
                return render(request, 'registdoc.html', context)
            elif 'nurse' in request.path:
                return render(request, 'registnurse.html', context)
            elif 'patient' in request.path:
                context['doctors'] = DoctorProfile.objects.all()
                return render(request, 'registpatient.html', context)

        except Exception as e:
            # Handle any other errors - KEEP THE FORM DATA
            print(f"Other error: {str(e)}")  # Debug print
            error_message = f"An error occurred: {str(e)}"
            
            # Create context with error message and preserve form data
            context = {
                'error': error_message,
                'request': request  # Pass request object to template
            }
            
            if 'doctor' in request.path:
                return render(request, 'registdoc.html', context)
            elif 'nurse' in request.path:
                return render(request, 'registnurse.html', context)
            elif 'patient' in request.path:
                context['doctors'] = DoctorProfile.objects.all()
                return render(request, 'registpatient.html', context)

    # Handle GET requests
    if 'doctor' in request.path:  
        return render(request, 'registdoc.html')  
    elif 'nurse' in request.path:  
        return render(request, 'registnurse.html')  
    elif 'patient' in request.path:  
        return render(request, 'registpatient.html', {'doctors': DoctorProfile.objects.all()})  
    else:
        return redirect('dashboard')
    
@login_required
@user_passes_test(is_admin, login_url='login')
def edit_doctor_profile(request, pk):
    doctor = get_object_or_404(DoctorProfile, user_id=pk)

    if request.user.role != 'Admin':
        return HttpResponseForbidden("You do not have permission to edit this profile.")
    
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            
            return redirect('listofdocs', doctor.id)
    else:
        form = DoctorProfileForm(instance=doctor)

    return render(request, 'edit_doctor_profile.html', {'form': form, 'doctor': doctor})

@login_required
@user_passes_test(is_admin, login_url='login')
def edit_nurse_profile(request, pk):
    nurse = get_object_or_404(NurseProfile, user_id=pk)

    # Only allow Admins to edit the profile
    if request.user.role != 'Admin':
        return HttpResponseForbidden("You do not have permission to edit this profile.")

    if request.method == 'POST':
        form = NurseProfileForm(request.POST, instance=nurse)
        if form.is_valid():
            form.save()
            return redirect('listofnurses', nurse.id) 
    else:
        form = NurseProfileForm(instance=nurse)

    return render(request, 'edit_nurse.html', {'form': form, 'nurse': nurse})


@login_required
@user_passes_test(is_admin, login_url='login')
def search_doctors(request):
    query = request.GET.get('q', '').strip()
    doctors = DoctorProfile.objects.all()

    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(departement__icontains=query)
        )

    doctor_info = [{
        'doctor': doc.user,
        'department': doc.departement
    } for doc in doctors]

    context = {
        'doctor_info': doctor_info,
        'query': query,
    }
    return render(request, 'docadmin.html', context)

@login_required
@user_passes_test(is_admin, login_url='login')
def search_nurses(request):
    query = request.GET.get('q', '').strip()
    nurses = NurseProfile.objects.all()

    if query:
        nurses = nurses.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(expertise__icontains=query)
        )

    nurse_info = [{
        'nurse': nurse.user,
        'expertise': nurse.expertise
    } for nurse in nurses]

    context = {
        'nurse_info': nurse_info,
        'query': query,
    }
    return render(request, 'nurseadmin.html', context)

@login_required
@user_passes_test(is_admin, login_url='login')
def search_patients(request):
    query = request.GET.get('q', '').strip()
    patients = PatientProfile.objects.select_related('user', 'assigned_doc__user').all()

    if query:
        patients = patients.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(gender__icontains=query) |
            Q(assigned_doc__user__first_name__icontains=query) |
            Q(assigned_doc__user__last_name__icontains=query)
        )

    patient_info = []
    for patient in patients:
        assigned_doc_name = None
        if patient.assigned_doc and patient.assigned_doc.user:
            assigned_doc_name = f"{patient.assigned_doc.user.first_name} {patient.assigned_doc.user.last_name}"

        patient_info.append({
            'patient': patient.user,
            'age': patient.age,
            'weight': patient.weight,
            'height': patient.height,
            'blood_type': patient.blood_type,
            'gender': patient.gender,
            'dieases': patient.dieases,
            'symptomps': patient.symptomps,
            'assigned_doc': assigned_doc_name,
        })

    context = {
        'patient_info': patient_info,
        'query': query,
    }
    return render(request, 'patientadmin.html', context)

@login_required
@user_passes_test(is_admin, login_url='login')
def search_activity_log(request):
    query = request.GET.get('q', '').strip()
    activity_logs = CustomUser.objects.all().order_by('-last_login')

    if query:
        # Try to match month name to month number
        month_map = {m.lower(): i for i, m in enumerate(calendar.month_name) if m}
        month_number = month_map.get(query.lower())

        # Build Q filters for username, name, role
        q_filter = (
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(role__icontains=query)
        )

        # If query matches a month name, also filter by last_login month
        if month_number:
            activity_logs = activity_logs.filter(q_filter | Q(last_login__month=month_number))
        else:
            activity_logs = activity_logs.filter(q_filter)

    context = {
        'activity_log': activity_logs[:10],
        'query': query,
    }
    return render(request, 'logactadmin.html', context)

@login_required
@user_passes_test(is_admin, login_url='login')
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)

    if user.role == 'Admin':
        messages.error(request='You cannot delete an Admin user.')
        return redirect('dashboard')

    if user.role == 'Doctor':
        try:
            doctor_profile = DoctorProfile.objects.get(user=user)
            # Set assigned_doc to None for all patients assigned to this doctor
            PatientProfile.objects.filter(assigned_doc=doctor_profile).update(assigned_doc=None)
        except DoctorProfile.DoesNotExist:
            pass  # Doctor profile doesn't exist, nothing to unassign

    user.delete()
    
    messages.success(request, f'User {user.username} has been deleted successfully.')
    return redirect('dashboard')  


