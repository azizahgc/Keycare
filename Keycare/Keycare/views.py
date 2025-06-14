from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.conf import settings
from.utils import send_otp
from datetime import datetime
import pyotp
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .utils import send_otp
from django.contrib.auth.models import User, Group
from django.contrib.admin.models import LogEntry
from accounts.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.cache import never_cache


def loginpage(request):
    error_message = None
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        print("Form submitted!")
        if form.is_valid():
            print("Form is valid")
            user = form.get_user()
            request.session['username'] = user.username
            send_otp(request)
            return redirect('otp')  # Make sure you have 'otp' view
        else:
            print("Form is not valid")
            print(form.errors)
            error_message = "Invalid username or password"
            return render(request, 'loginpage.html', {'error_message': error_message}) 
    else:
        form = AuthenticationForm()
        return render(request, 'loginpage.html')

      
@never_cache
def otp_view(request):
    error_message = None

    if request.method == "POST":
        otp = request.POST.get('otp')
        username = request.session.get('username')
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_until = request.session.get('otp_valid_date')

        print(f"Username: {username}")
        print(f"OTP Secret Key: {otp_secret_key}")
        print(f"OTP Valid Until (raw): {otp_valid_until}")
        print(f"Current Time: {datetime.now()}")
        
        if 'resend_otp' in request.POST:
            send_otp(request)
            error_message = "A new OTP has been sent to your email."
        elif username and otp_secret_key and otp_valid_until:
            try:
                valid_until = datetime.fromisoformat(otp_valid_until)
                print(f"OTP Valid Until (parsed): {valid_until}")

                if valid_until > datetime.now():
                    print("OTP is within valid time window")

                    totp = pyotp.TOTP(otp_secret_key, interval=300)
                    expected_otp = totp.now()
                    print(f"Expected OTP: {expected_otp}")
                    print(f"Entered OTP: {otp}")

                    if totp.verify(otp, valid_window=1):
                        print("OTP Verified Successfully!")
                        user = get_object_or_404(CustomUser, username=username)
                        print(user.username)
                        login(request, user)

                        for key in ['otp_secret_key', 'otp_valid_date', 'username']:
                            if key in request.session:
                                del request.session[key]
                        
                        if user.role == 'Doctor':
                            return redirect('doctordashboard')  
                        elif user.role == 'Admin':
                            return redirect('dashboard')  
                        elif user.role == 'Nurse':
                            return redirect('nursedashboard')
                        elif user.role == 'Patient':
                            return redirect('patientdashboard')
    
                    else:
                        error_message = "Invalid OTP"
                else:
                    error_message = "OTP has expired"
            except Exception as e:
                print(f"Error parsing datetime or verifying OTP: {e}")
                error_message = "Something went wrong while processing OTP"
        else:
            error_message = "Missing OTP session data. Please try again."

    return render(request, 'otp.html', {'error_message': error_message})

def resend_otp(request):
    if request.method == "POST":
        username = request.session.get('username')
        if username:
            send_otp(request)  # Resend OTP
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)

@login_required  # Ensures that only authenticated users can access the logout view
@never_cache  # Prevents caching of this view
def logout_view(request):
    # Invalidate the session to prevent session fixation attacks
    logout(request)
    request.session.flush()  # Ensure the session is completely cleared

    # Redirect to the login page
    response = redirect('login')

    # Set headers to prevent caching of the response (important to prevent using the back button)
    response['Cache-Control'] = 'no-store'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response
    