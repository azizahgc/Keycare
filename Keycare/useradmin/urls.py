from django.urls import path
from .views import  listofdoc_view, nurseadmin_view, patientadmin_view, dashboard_view, logactadmin_view, register_user, edit_doctor_profile, edit_nurse_profile, listofdoctor_view, nurseadmin2_view, patientadmin2_view, search_doctors
from .views import search_nurses, search_patients, search_activity_log,  delete_user




urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('listofdoc/', listofdoc_view, name= 'listofdoc'),
    path('listofnurse/', nurseadmin_view, name= 'listofnurse'),
    path('listofpatient/', patientadmin_view, name= 'listofpatient'),
    path('listofpatients/<int:pk>', patientadmin2_view, name='listofpatients'),
    path('logactadmin/', logactadmin_view, name= 'logactadmin'),
    path('register/doctor/', register_user, name='registdoc'),
    path('register/nurse/', register_user, name='registnurse'),
    path('register/patient/', register_user, name='registpatient'),
    path('doctor/<int:doctor_id>/edit/', edit_doctor_profile, name='edit_doctor_profile'),
    path('listofdocs/<int:pk>/', listofdoctor_view, name='listofdocs'),
    path('nurse/<int:nurse_id>/edit/', edit_nurse_profile, name='edit_nurse_profile'),
    path('listofnurses/<int:pk>/', nurseadmin2_view, name= 'listofnurses'),
    path('doctors_list/', search_doctors, name='doctors_list'),
    path('nurses_list/', search_nurses, name='nurses_list'),
    path('patients_list/', search_patients, name='patients_list'),
    path('activity_log/', search_activity_log, name='activity_log'),
    path('delete_user/<int:pk>/', delete_user, name='delete_user'),
]