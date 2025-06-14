"""
URL configuration for Keycare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .import views
from useradmin.views import dashboard_view, listofdoc_view, nurseadmin_view, nurseadmin2_view, patientadmin2_view, listofdoctor_view, patientadmin_view, logactadmin_view, register_user, edit_nurse_profile, edit_doctor_profile, search_doctors, delete_user
from useradmin.views import search_nurses, search_patients, search_activity_log
from userdoctor.views import dashdoc_view, patientdoc_view, docpatientprofile_view
from usernurse.views import dashnurse_view, patientnurse_view, patientview_view
from userpatient.views import dashpatient_view, docpatient_view, patient_view, change_doctor, edit_patient_profile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.loginpage, name= 'login'),
    path('otp/', views.otp_view, name='otp'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('useradmin/', include('useradmin.urls')),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('listofdoc/', listofdoc_view,name= 'listofdoc'),
    path('listofnurse/', nurseadmin_view,name= 'listofnurse'),
    path('listofpatient/', patientadmin_view, name= 'listofpatient'),
    path('listofpatients/<int:pk>', patientadmin2_view, name='listofpatients'),
    path('logactadmin/', logactadmin_view, name= 'logactadmin'),
    path('delete_user/<int:pk>/', delete_user, name='delete_user'),
    path('register/doctor/', register_user, name='registdoc'),
    path('register/nurse/', register_user, name='registnurse'),
    path('register/patient/', register_user, name='registpatient'),
    path('edit_nurse_profile/<int:pk>/', edit_nurse_profile, name='edit_nurse_profile'),
    path('listofnurses/<int:pk>/', nurseadmin2_view, name= 'listofnurses'),
    path('listofdocs/<int:pk>/', listofdoctor_view, name='listofdocs'),
    path('edit_doctor_profile/<int:pk>/', edit_doctor_profile, name='edit_doctor_profile'),
    path('doctors_list/', search_doctors, name='doctors_list'),
    path('nurses_list/', search_nurses, name='nurses_list'),
    path('patients_list/', search_patients, name='patients_list'),
    path('activity_log/', search_activity_log, name='activity_log'),
    path('userdoctor/', include('userdoctor.urls')),
    path('doctordashboard/', dashdoc_view, name='doctordashboard'),
    path('patientdoc/', patientdoc_view, name='patientdoc'),
    path('doctor/<int:pk>/', docpatientprofile_view, name='doctor'),
    path('usernurse/', include('usernurse.urls')),
    path('nursedashboard/', dashnurse_view, name='nursedashboard'),
    path('patientnurse/', patientnurse_view, name='patientnurse'),
    path('patientviews/<int:pk>', patientview_view, name='patientviews'),
    path('userpatient/', include('userpatient.urls')),
    path('patientdashboard/', dashpatient_view, name='patientdashboard'),
    path('listofdoct/', docpatient_view, name= 'listofdoct'),
    path('patient/', patient_view, name='patient'),
    path('changedoctor/', change_doctor, name='changedoctor'),
    path('edit_patient_profile/', edit_patient_profile, name='edit_patient_profile'),
]
