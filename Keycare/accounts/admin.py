from django.contrib import admin
from .models import PatientProfile, CustomUser, DoctorProfile, NurseProfile

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    search_fields = ('username', 'email', 'role')

admin.site.register(CustomUser)
admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)
admin.site.register(PatientProfile) 