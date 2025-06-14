import pyotp
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from accounts.models import CustomUser


def send_otp(request):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=5)
    request.session['otp_valid_date'] = str(valid_date)

    print(f" Your One Time Password is {otp}")
    
    username = request.session['username']  
    if not username:
        print("No username found in session.")
        return  

    user = get_object_or_404(CustomUser, username=username)
    user_email = user.email

    send_mail(
        subject='Your One-Time Password (OTP)',  # Email subject
        message=f'Your OTP code is: {otp}. It will expire in 5 minutes.',  # Email body
        from_email=settings.DEFAULT_FROM_EMAIL,  # From email (configured in settings)
        recipient_list=[user_email],  # Recipient's email
    )

    print(f"OTP for {username}: {otp}")