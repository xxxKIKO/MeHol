from django.contrib import admin
from .models import Medico,Paciente

# Register your models here.
class MedicoAdmin(admin.ModelAdmin):
    pass
admin.site.register(Medico, MedicoAdmin)

class PacienteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Paciente, PacienteAdmin)
"""
class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)
"""