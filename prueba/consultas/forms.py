from django import forms
from django.contrib.auth.models import User
from . import models



#inicio de sesion de asistente
class AsistenteSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#inicio de sesion de medico
class MedicoUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class MedicoForm(forms.ModelForm):
    class Meta:
        model=models.Medico
        fields=['domicilio','celular','especialidad','status','foto']



#inicio de sesion de paciente
class PacienteUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PacienteForm(forms.ModelForm):
    medicoAsignadoId=forms.ModelChoiceField(queryset=models.Medico.objects.all().filter(status=True),empty_label="Médico y Especialidad", to_field_name="user_id")
    nombreTutor: forms.CharField(required=False)
    apellidosTutor: forms.CharField(required=False)
    telefonoTutor: forms.CharField(required=False)
    celularTutor: forms.CharField(required=False)
    class Meta:
        widgets = {
        'fechaNac': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        model=models.Paciente
        fields=['domicilio','poblacion','municipio','entidad','pais','telefono','apmaterno','fechaNac','celular','correo','facebook','instagram','pagweb','status','sintomas','foto','nombreTutor','apellidosTutor','telefonoTutor','celularTutor']



class CitasForm(forms.ModelForm):
    medicoId=forms.ModelChoiceField(queryset=models.Medico.objects.all().filter(status=True),empty_label="Nombre del Médico", to_field_name="user_id")
    pacienteId=forms.ModelChoiceField(queryset=models.Paciente.objects.all().filter(status=True),empty_label="Paciente y Síntomas", to_field_name="user_id")
    class Meta:
        widgets = {
            'fechaCita': forms.DateTimeInput(attrs={'type': 'datetime-local','step': '1800'},format='%Y-%m-%dT%H:00:00')
        }
        model=models.Citas
        fields=['descripcion','status','fechaCita','ciudadCita']

    def __str__(self):
        return self.pacienteId

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = models.Consulta
        fields = ['sintomas', 'diagnostico', 'tratamiento']

    def __str__(self):
        return self.pacienteId

class PacienteCitasForm(forms.ModelForm):
    medicoId=forms.ModelChoiceField(queryset=models.Medico.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Citas
        fields=['descripcion','status']



#for contact us page
class ContactusForm(forms.Form):
    Nombre = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Mensaje = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


