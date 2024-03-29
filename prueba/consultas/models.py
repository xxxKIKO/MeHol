from django.db import models
from datetime import datetime, date
from django.contrib.auth.models import User



especialidades=[('Cardiologo','Cardiologo'),
('Dermatologo','Dermatologo'),
('Alergologo','Alergologo'),
('Anestesiologo','Anestesiologo'),
('Holístico','Holístico')
]
class Medico(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotosdeperfil/fotosdeperfilmedicos/',null=True,blank=True)
    domicilio = models.CharField(max_length=40)
    celular = models.CharField(max_length=20,null=True)
    especialidad = models.CharField(max_length=50,choices=especialidades,default='Holístico')
    status =models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.especialidad)



class Paciente(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE)
    apmaterno=models.CharField(max_length=20,null=False, default='')
    fechaNac=models.DateField(default=date.today)
    domicilio = models.CharField(max_length=40,default='')
    poblacion = models.CharField(max_length=20,default='')
    municipio = models.CharField(max_length=20,default='')
    entidad = models.CharField(max_length=20,default='')
    pais = models.CharField(max_length=20,default='')
    telefono = models.CharField(max_length=20,null=False,default='')
    celular = models.CharField(max_length=20,null=False, default='')
    sintomas = models.CharField(max_length=100,null=False,default='')
    medicoAsignadoId = models.PositiveIntegerField(null=True)
    correo = models.CharField(max_length=40,default='')
    facebook = models.CharField(max_length=40,default='')
    instagram = models.CharField(max_length=40,default='')
    pagweb = models.CharField(max_length=40,default='')
    fechadeadmision =models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    nombreTutor = models.CharField(max_length=30, blank=True, null=True, default='')
    apellidosTutor = models.CharField(max_length=30, blank=True, null=True, default='')
    telefonoTutor = models.CharField(max_length=20, blank=True, null=True, default='')
    celularTutor = models.CharField(max_length=20, blank=True, null=True, default='')
    foto = models.ImageField(upload_to='fotosdeperfil/fotosdeperfilpacientes/',null=True,blank=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.sintomas+")"

ciudades=[('Colima','Colima'),
          ('Guadalajara', 'Guadalajara'),
          ('Tijuana','Tijuana'),
          ('México','México'),
          ('Monterrey','Monterrey'),
          ('Cd. Guzman','Cd. Guzman'),
]
class Citas(models.Model):
    idCita = models.AutoField(primary_key=True)
    pacienteId=models.ForeignKey(Paciente, on_delete=models.CASCADE, default=0)
    medicoId=models.ForeignKey(Medico, on_delete=models.CASCADE, default=0)
    pacienteNombre=models.CharField(max_length=40,null=True)
    medicoNombre=models.CharField(max_length=40,null=True)
    fechaCita=models.DateTimeField(default=datetime.now)
    ciudadCita=models.CharField(max_length=40, choices=ciudades, default='Colima')
    descripcion=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    ejecutada=models.BooleanField(default=False)
    cobrada=models.BooleanField(default=False)


class Consulta(models.Model):
    idConsulta = models.AutoField(primary_key=True)
    pacienteId = models.ForeignKey(Paciente, on_delete=models.CASCADE, default=0)
    medicoId = models.ForeignKey(Medico, on_delete=models.CASCADE, default=0)
    idCita = models.ForeignKey(Citas, on_delete=models.CASCADE, default=0)
    fechaCita = models.DateTimeField(default=datetime.now)
    sintomas = models.TextField(max_length=500)
    diagnostico = models.TextField(max_length=500)
    tratamiento = models.TextField(max_length=500)
    

class CuentaPaciente(models.Model):
    idCita=models.ForeignKey(Citas, on_delete=models.CASCADE, default=0)
    pacienteId=models.ForeignKey(Paciente, on_delete=models.CASCADE, default=0)
    pacienteNombre=models.CharField(max_length=40)
    medicoAsignadoNombre=models.CharField(max_length=40)
    medicoAsignadoApellido=models.CharField(max_length=40, default="")
    domicilio = models.CharField(max_length=40)
    celular = models.CharField(max_length=20,null=True)
    sintomas = models.CharField(max_length=100,null=True)

    fechaAdmision=models.DateField(null=False)
    fechaAlta=models.DateField(null=False)
    diasTranscurridos=models.PositiveIntegerField(null=False)

    habitacion=models.PositiveIntegerField(null=False)
    medicamenteos=models.PositiveIntegerField(null=False)
    costomedico=models.PositiveIntegerField(null=False)
    otroscargos=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
