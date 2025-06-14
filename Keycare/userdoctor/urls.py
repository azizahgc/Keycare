from django.urls import path
from .views import dashdoc_view, patientdoc_view, docpatientprofile_view



urlpatterns = [
    path('doctordashboard/', dashdoc_view, name='doctordashboard'),
    path('patientdoc/', patientdoc_view, name='patientdoc'),
    path('doctor/<int:pk>/', docpatientprofile_view, name='doctor'),
    path('patientdoc/<int:pk>', patientdoc_view, name='patientdoc'),
]
