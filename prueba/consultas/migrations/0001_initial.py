# Generated by Django 3.2.17 on 2023-05-03 21:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Citas',
            fields=[
                ('idCita', models.AutoField(primary_key=True, serialize=False)),
                ('pacienteId', models.PositiveIntegerField(null=True)),
                ('medicoId', models.PositiveIntegerField(null=True)),
                ('pacienteNombre', models.CharField(max_length=40, null=True)),
                ('medicoNombre', models.CharField(max_length=40, null=True)),
                ('fechaCita', models.DateTimeField(default=datetime.datetime.now)),
                ('descripcion', models.TextField(max_length=500)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CuentaPaciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pacienteId', models.PositiveIntegerField(null=True)),
                ('pacienteNombre', models.CharField(max_length=40)),
                ('medicoAsignadoNombre', models.CharField(max_length=40)),
                ('medicoAsignadoApellido', models.CharField(default='', max_length=40)),
                ('domicilio', models.CharField(max_length=40)),
                ('celular', models.CharField(max_length=20, null=True)),
                ('sintomas', models.CharField(max_length=100, null=True)),
                ('fechaAdmision', models.DateField()),
                ('fechaAlta', models.DateField()),
                ('diasTranscurridos', models.PositiveIntegerField()),
                ('habitacion', models.PositiveIntegerField()),
                ('medicamenteos', models.PositiveIntegerField()),
                ('costomedico', models.PositiveIntegerField()),
                ('otroscargos', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotosdeperfil/fotosdeperfilpacientes/')),
                ('domicilio', models.CharField(max_length=40)),
                ('celular', models.CharField(max_length=20)),
                ('sintomas', models.CharField(max_length=100)),
                ('medicoAsignadoId', models.PositiveIntegerField(null=True)),
                ('fechadeadmision', models.DateField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Medico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotosdeperfil/fotosdeperfilmedicos/')),
                ('domicilio', models.CharField(max_length=40)),
                ('celular', models.CharField(max_length=20, null=True)),
                ('especialidad', models.CharField(choices=[('Cardiologo', 'Cardiologo'), ('Dermatologo', 'Dermatologo'), ('Alergologo', 'Alergologo'), ('Anestesiologo', 'Anestesiologo'), ('Holístico', 'Holístico')], default='Holístico', max_length=50)),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]