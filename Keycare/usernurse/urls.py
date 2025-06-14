from django.urls import path
from .views import dashnurse_view, patientnurse_view, patientview_view

urlpatterns = [
    path('nursedashboard/', dashnurse_view, name='nursedashboard'),   
    path('patientnurse/', patientnurse_view, name='patientnurse' ),
    path('patientsview/<int:pk>', patientview_view, name='patientsview')
]
