from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings
from .models import Citas
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from .forms import ConsultaForm
from .models import Citas, Consulta

import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


# Vista de inicio
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')

#para mostrar la vista de asistente
def asistenteclick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'asistenteclick.html')


#para mostrar la vista de medico
def medicoclick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'medicoclick.html')


#para mostrar la vista de paciente
def pacienteclick(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'pacienteclick.html')

#para mostrar la vista de asistente despues de loguearse
def asistentesignup(request):
    form=forms.AsistenteSigupForm()
    if request.method=='POST':
        form=forms.AsistenteSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('asistentelogin')
    return render(request,'asistentesignup.html',{'form':form})

#para mostrar la vista de medico despues de loguearse
def medicosignup(request):
    userForm=forms.MedicoUserForm()
    medicoForm=forms.MedicoForm()
    mydict={'userForm':userForm,'medicoForm':medicoForm}
    if request.method=='POST':
        userForm=forms.MedicoUserForm(request.POST)
        medicoForm=forms.MedicoForm(request.POST,request.FILES)
        if userForm.is_valid() and medicoForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            medico=medicoForm.save(commit=False)
            medico.user=user
            medico=medico.save()
            my_doctor_group = Group.objects.get_or_create(name='MEDICO')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('medicologin')
    return render(request,'medicosignup.html',context=mydict)

#para mostrar la vista de paciente despues de loguearse
def pacientesignup(request):
    userForm=forms.PacienteUserForm()
    pacienteForm=forms.PacienteForm()
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            paciente=pacienteForm.save(commit=False)
            paciente.user=user
            paciente.medicoAsignadoId=request.POST.get('medicoAsignadoId')
            paciente=paciente.save()
            my_patient_group = Group.objects.get_or_create(name='PACIENTE')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('pacientelogin')
    return render(request,'pacientesignup.html',context=mydict)

#vistas para contact us y about us
def aboutus_view(request):
    return render(request,'aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Nombre']
            message = sub.cleaned_data['Mensaje']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'contactussuccess.html')
    return render(request, 'contactus.html', {'form':sub})

#depues de hacer login es necesario comprobar lo siguiente
#para saber si es asistente, medico o paciente
def is_asistente(user):
    return user.groups.filter(name='ADMIN').exists()
def is_medico(user):
    return user.groups.filter(name='MEDICO').exists()
def is_paciente(user):
    return user.groups.filter(name='PACIENTE').exists()


#---------esta vista permite redireccionar según el tipo de usuario, asistente, médico o paciente
def afterlogin_view(request):
    if is_asistente(request.user):
        return redirect('asistente_dashboard')
    elif is_medico(request.user):
        accountapproval=models.Medico.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('medico_dashboard')
        else:
            return render(request,'doctor_wait_for_approval.html')
    elif is_paciente(request.user):
        accountapproval=models.Paciente.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('paciente_dashboard')
        else:
            return render(request,'patient_wait_for_approval.html')

#---------------------------------------------------------------------------------
#------------------------ COMIENZAN LAS VISTAS DEL ASISTENTE----------------------
#---------------------------------------------------------------------------------
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_dashboard_view(request):
    #for both table in admin dashboard
    medicos=models.Medico.objects.all().order_by('-id')
    pacientes=models.Paciente.objects.all().order_by('-id')
    #for three cards
    medicoscount=models.Medico.objects.all().filter(status=True).count()
    medicopendientecount=models.Medico.objects.all().filter(status=False).count()

    pacientecount=models.Paciente.objects.all().filter(status=True).count()
    pacientependientecount=models.Paciente.objects.all().filter(status=False).count()


    citascount=models.Citas.objects.all().filter(status=True).count()
    citaspenientescount=models.Citas.objects.all().filter(status=False).count()
    milista={
    'medicos':medicos,
    'pacientes':pacientes,
    'medicoscount':medicoscount,
    'medicopendientecount':medicopendientecount,
    'pacientecount':pacientecount,
    'pacientependientecount':pacientependientecount,
    'citascount':citascount,
    'citaspenientescount':citaspenientescount,
    }
    return render(request,'asistente_dashboard.html',context=milista)

# para cargar la vista de menú de médicos
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_medicos_view(request):
    return render(request,'asistente_menu_medicos.html')

#para cargar la vista de aprobar médico
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_aprobar_medico_view(request):
    #those whose approval are needed
    medicos=models.Medico.objects.all().filter(status=False)
    return render(request,'asistente_aprobar_medico.html',{'medicos':medicos})

#para arpobar el médico
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def aprobar_medico_view(request,pk):
    medico=models.Medico.objects.get(id=pk)
    medico.status=True
    medico.save()
    return redirect(reverse('asistente_aprobar_medico'))

#para rechazar el médico
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def rechazar_medico_view(request,pk):
    medico=models.Medico.objects.get(id=pk)
    user=models.User.objects.get(id=medico.user_id)
    user.delete()
    medico.delete()
    return redirect('asistente_aprobar_medico')


#para cargar la vista de menú de pacientes
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_menu_pacientes_view(request):
    return render(request,'asistente_menu_pacientes.html')

#vista para aprobar pacientes
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_aprobar_paciente_view(request):
    #those whose approval are needed
    pacientes=models.Paciente.objects.all().filter(status=False)
    return render(request,'asistente_aprobar_paciente.html',{'pacientes':pacientes})


#aprobar el paciente
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def aprobar_paciente_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    paciente.status=True
    paciente.save()
    return redirect(reverse('asistente_aprobar_paciente'))


#rechazar el paciente
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def rechazar_paciente_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)
    user.delete()
    paciente.delete()
    return redirect('asistente_aprobar_paciente')

#asistente agrega un medico
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_agregar_medico_view(request):
    userForm=forms.MedicoUserForm()
    medicoForm=forms.MedicoForm()
    mydict={'userForm':userForm,'medicoForm':medicoForm}
    if request.method=='POST':
        userForm=forms.MedicoUserForm(request.POST)
        medicoForm=forms.MedicoForm(request.POST, request.FILES)
        if userForm.is_valid() and medicoForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            medico=medicoForm.save(commit=False)
            medico.user=user
            medico.status=True
            medico.save()

            my_doctor_group = Group.objects.get_or_create(name='MEDICO')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('asistente_menu_medicos')
    return render(request,'asistente_agregar_medico.html',context=mydict)

#vista para la lista de medicos
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_lista_medicos_view(request):
    medicos=models.Medico.objects.all().filter(status=True)
    return render(request,'asistente_lista_medicos.html',{'medicos':medicos})



@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def eliminar_medico_view(request,pk):
    medico=models.Medico.objects.get(id=pk)
    user=models.User.objects.get(id=medico.user_id)
    user.delete()
    medico.delete()
    return redirect('asistente_menu_medicos')



@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def actualizar_medico_view(request,pk):
    medico=models.Medico.objects.get(id=pk)
    user=models.User.objects.get(id=medico.user_id)

    userForm=forms.MedicoUserForm(instance=user)
    medicoForm=forms.MedicoForm(request.FILES,instance=medico)
    mydict={'userForm':userForm,'medicoForm':medicoForm}
    if request.method=='POST':
        userForm=forms.MedicoUserForm(request.POST,instance=user)
        medicoForm=forms.MedicoForm(request.POST,request.FILES,instance=medico)
        if userForm.is_valid() and medicoForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            medico=medicoForm.save(commit=False)
            medico.status=True
            medico.save()
            return redirect('asistente_lista_medicos')
    return render(request,'actualizar_medico.html',context=mydict)

#vista para ver la lista de médicos por especialidad
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_medico_especialidad_view(request):
    medicos=models.Medico.objects.all().filter(status=True)
    return render(request,'asistente_medico_especialidad.html',{'medicos':medicos})


#vista para agregar un paciente
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_agregar_paciente_view(request):
    userForm=forms.PacienteUserForm()
    pacienteForm=forms.PacienteForm()
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            paciente=pacienteForm.save(commit=False)
            paciente.user=user
            paciente.status=True

            menor_de_edad = request.POST.get('menorEdadCheckbox') == 'on'
            if not menor_de_edad:
                paciente.nombreTutor = None
                paciente.apellidosTutor = None
                paciente.telefonoTutor = None
                paciente.celularTutor = None
            paciente.medicoAsignadoId=request.POST.get('medicoAsignadoId')
            paciente.save()

            my_patient_group = Group.objects.get_or_create(name='PACIENTE')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('asistente_menu_pacientes')
    return render(request,'asistente_agregar_paciente.html',context=mydict)

#vista para la lista de pacientes que puede ver el asistente
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_lista_pacientes_view(request):
    pacientes=models.Paciente.objects.all().filter(status=True)
    return render(request,'asistente_lista_pacientes.html',{'pacientes':pacientes})

#vista para eliminar paciente definitivamente
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def eliminar_paciente_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)
    user.delete()
    paciente.delete()
    return redirect('asistente_lista_pacientes')


#vista para actualizar los datos del paciente
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def actualizar_paciente_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    user=models.User.objects.get(id=paciente.user_id)

    userForm=forms.PacienteUserForm(instance=user)
    pacienteForm=forms.PacienteForm(request.FILES,instance=paciente)
    mydict={'userForm':userForm,'pacienteForm':pacienteForm}
    if request.method=='POST':
        userForm=forms.PacienteUserForm(request.POST,instance=user)
        pacienteForm=forms.PacienteForm(request.POST,request.FILES,instance=paciente)
        if userForm.is_valid() and pacienteForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            paciente=pacienteForm.save(commit=False)
            paciente.status=True
            paciente.medicoAsignadoId=request.POST.get('medicoAsignadoId')
            paciente.save()
            return redirect('asistente_lista_pacientes')
    return render(request,'actualizar_paciente.html',context=mydict)


#--------------------- ESTAS VISTAS SON PARA GENERAR LA CUENTA DEL PACIENTE AL DARLO DE ALTA-------------------------
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_alta_paciente_view(request):
    paciente=models.Paciente.objects.all().filter(status=True)
    return render(request,'asistente_alta_paciente.html',{'pacientes':paciente})



@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def alta_paciente_view(request,pk):
    paciente=models.Paciente.objects.get(id=pk)
    cita=models.Citas.objects.get(pacienteId__user__id=paciente.user.id)
    dias=(date.today()-paciente.fechadeadmision) #2 days, 0:00:00
    medicoAsignado=models.User.objects.all().filter(id=paciente.medicoAsignadoId)
    d=dias.days # only how many day that is 2
    patientDict={
        'pacienteId':pk,
        'nombre':paciente.get_name,
        'celular':paciente.celular,
        'domicilio':paciente.domicilio,
        'sintomas':paciente.sintomas,
        'fechadeadmision':paciente.fechadeadmision,
        'hoy':date.today(),
        'dias':d,
        'nombreMedicoAsignado':medicoAsignado[0].first_name,
        'apellidoMedicoAsignado':medicoAsignado[0].last_name,
    }
    if request.method == 'POST':
        feeDict ={
            'habitacioncargo':int(request.POST['habitacioncargo'])*int(d),
            'medicocargo':request.POST['medicocargo'],
            'medicamentocargo' : request.POST['medicamentocargo'],
            'otrocargo' : request.POST['otrocargo'],
            'total':(int(request.POST['habitacioncargo'])*int(d))+int(request.POST['medicocargo'])+int(request.POST['medicamentocargo'])+int(request.POST['otrocargo'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.CuentaPaciente()
        pDD.idCita=cita
        pDD.pacienteId=paciente
        pDD.pacienteNombre=paciente.get_name
        pDD.medicoAsignadoNombre=medicoAsignado[0].first_name
        pDD.medicoAsignadoApellido=medicoAsignado[0].last_name
        pDD.domicilio=paciente.domicilio
        pDD.celular=paciente.celular
        pDD.sintomas=paciente.sintomas
        pDD.fechaAdmision=paciente.fechadeadmision
        pDD.fechaAlta=date.today()
        pDD.diasTranscurridos=int(d)
        pDD.medicamenteos=int(request.POST['medicamentocargo'])
        pDD.habitacion=int(request.POST['habitacioncargo'])*int(d)
        pDD.costomedico=int(request.POST['medicocargo'])
        pDD.otroscargos=int(request.POST['otrocargo'])
        pDD.total=(int(request.POST['habitacioncargo'])*int(d))+int(request.POST['medicocargo'])+int(request.POST['medicamentocargo'])+int(request.POST['otrocargo'])
        pDD.save()
        return render(request,'paciente_cuenta_final.html',context=patientDict)
    return render(request,'paciente_generar_cuenta.html',context=patientDict)



#--------------para la cuenta del paciente, convertir a pdf y descargar
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def paciente_descarga_cuenta_view(request,pk):
    CuentaPaciente=models.CuentaPaciente.objects.all().filter(pacienteId=pk).order_by('-id')[:1]
    dict={
        'nombrePaciente':CuentaPaciente[0].pacienteNombre,
        'medicoAsignadoNombre':CuentaPaciente[0].medicoAsignadoNombre,
        'apellidoMedicoAsignado':CuentaPaciente[0].medicoAsignadoApellido,
        'domicilio':CuentaPaciente[0].domicilio,
        'celular':CuentaPaciente[0].celular,
        'sintomas':CuentaPaciente[0].sintomas,
        'fechadeAdmision':CuentaPaciente[0].fechaAdmision,
        'fechaAlta':CuentaPaciente[0].fechaAlta,
        'diastranscurridos':CuentaPaciente[0].diasTranscurridos,
        'medicamentocargo':CuentaPaciente[0].medicamenteos,
        'habitacioncargo':CuentaPaciente[0].habitacion,
        'medicocargo':CuentaPaciente[0].costomedico,
        'otroscargo':CuentaPaciente[0].otroscargos,
        'total':CuentaPaciente[0].total,
    }
    return render_to_pdf('descargar_cuenta.html',dict)

#desde aqui son las vistas para cobrar la cita------------------------------
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_cobrar_cita_view(request,pk):
    d=0
    cita=models.Citas.objects.get(idCita=pk)
    medico=cita.medicoId
    paciente=cita.pacienteId
    listaDatos={
        'idCita':cita.idCita,
        'pacienteNombre':paciente.user.first_name,
        'pacienteApellido':paciente.user.last_name,
        'medicoNombre':medico.user.first_name,
        'medicoApellido':medico.user.last_name,
        'celular':paciente.celular,
        'domicilio':paciente.domicilio,
        'sintomas':paciente.sintomas,
        'fechaCita':cita.fechaCita,
        'hoy':date.today(),
    }
    if request.method == 'POST':
        listaCargos ={
            'medicocargo':request.POST['medicocargo'],
            'medicamentocargo' : request.POST['medicamentocargo'],
            'otrocargo' : request.POST['otrocargo'],
            'total':int(request.POST['medicocargo'])+int(request.POST['medicamentocargo'])+int(request.POST['otrocargo'])
        }
        listaDatos.update(listaCargos)
        #para actualizar la base de datos de la cuenta del paciente
        pDD=models.CuentaPaciente()
        pDD.idCita=cita
        pDD.pacienteId=paciente
        pDD.pacienteNombre=paciente.get_name
        pDD.medicoAsignadoNombre=medico.user.first_name
        pDD.medicoAsignadoApellido=medico.user.last_name
        pDD.domicilio=paciente.domicilio
        pDD.celular=paciente.celular
        pDD.sintomas=paciente.sintomas
        pDD.fechaAdmision=paciente.fechadeadmision
        pDD.fechaAlta=cita.fechaCita
        pDD.diasTranscurridos=int(d)
        pDD.medicamenteos=int(request.POST['medicamentocargo'])
        pDD.habitacion=int(d)
        pDD.costomedico=int(request.POST['medicocargo'])
        pDD.otroscargos=int(request.POST['otrocargo'])
        pDD.total=int(request.POST['medicocargo'])+int(request.POST['medicamentocargo'])+int(request.POST['otrocargo'])
        pDD.save()
        cita.cobrada=True
        cita.save()
        return render(request,'asistente_cobrar_cita_final.html',context=listaDatos)
    return render(request,'asistente_cobrar_cita.html',context=listaDatos)



#--------------para la cuenta del paciente, convertir a pdf y descargar



def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def asistente_descarga_cobro_view(request,pk):
    CuentaPaciente=models.CuentaPaciente.objects.get(idCita=pk)
    dict={
        'idCita':pk,
        'nombrePaciente':CuentaPaciente.pacienteNombre,
        'medicoAsignadoNombre':CuentaPaciente.medicoAsignadoNombre,
        'apellidoMedicoAsignado':CuentaPaciente.medicoAsignadoApellido,
        'domicilio':CuentaPaciente.domicilio,
        'celular':CuentaPaciente.celular,
        'sintomas':CuentaPaciente.sintomas,
        'fechadeAdmision':CuentaPaciente.fechaAdmision,
        'fechaAlta':CuentaPaciente.fechaAlta,
        'diastranscurridos':CuentaPaciente.diasTranscurridos,
        'medicamentocargo':CuentaPaciente.medicamenteos,
        'habitacioncargo':CuentaPaciente.habitacion,
        'medicocargo':CuentaPaciente.costomedico,
        'otroscargo':CuentaPaciente.otroscargos,
        'total':CuentaPaciente.total,
    }
    #pdf = render_to_pdf('mostrarpdf.html', dict)
    #response = HttpResponse(pdf, content_type='application/pdf')
    #response['Content-Disposition'] = 'inline; filename="cobro_cita.pdf"'
    #citasporcobrar_url = reverse('asistente_citasporcobrar')
    #return render(request, 'mostrarpdf.html', {'pdf_url': response, 'citasporcobrar_url': citasporcobrar_url})
    response = render_to_pdf('mostrarpdf.html',dict)
    return response


# ------------- aqui empiezan las vistas de las citas
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_menu_citas_view(request):
    return render(request,'asistente_menu_citas.html')



@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_ver_citas_view(request):
    citas=models.Citas.objects.all().filter(status=True).order_by('-idCita')
    return render(request,'asistente_ver_citas.html',{'citas':citas})



@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)

#esta es la funcion nueva:
def asistente_agregar_citas_view(request):
    if request.method == 'POST':
        citas_form = forms.CitasForm(request.POST)
        if citas_form.is_valid():
            # Convertir la fecha de cita de cadena a datetime
            fecha_cita = datetime.strptime(request.POST['fechaCita'], '%Y-%m-%dT%H:%M')

            try:
                validar_cita(request.POST['medicoId'], fecha_cita)
            except ValidationError as error:
                # Mostrar el mensaje de error personalizado
                messages.add_message(request, messages.WARNING, 'El horario ya está ocupado. Por favor, seleccione un horario diferente.')

            else:
                cita = citas_form.save(commit=False)
                medico = models.Medico.objects.get(user_id=request.POST['medicoId'])
                cita.medicoId = medico
                paciente = models.Paciente.objects.get(user_id=request.POST['pacienteId'])
                cita.pacienteId = paciente
                cita.medicoNombre = medico.user.first_name
                cita.pacienteNombre = paciente.user.first_name
                cita.fechaCita = request.POST.get('fechaCita')
                cita.status = True
                cita.save()

                return HttpResponseRedirect(reverse('asistente_ver_citas'))

    else:
        citas_form = forms.CitasForm()

    context = {
        'CitasForm': citas_form,
    }
    return render(request, 'asistente_agregar_cita.html', context)

from django.core.exceptions import ValidationError
def validar_cita(medico_id, fecha_cita):
    # Verificar si ya existe una cita programada para ese médico en esa fecha y hora
    citas_programadas = Citas.objects.filter(medicoId__user__id=medico_id, fechaCita=fecha_cita)
    if citas_programadas.exists():
        raise ValidationError("El horario ya está ocupado. Por favor, seleccione un horario diferente.")
    return True


@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_aprobar_citas_view(request):
    #those whose approval are needed
    citas=models.Citas.objects.all().filter(status=False)
    return render(request,'asistente_aprobar_cita.html',{'citas':citas})



@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def aprobar_cita_view(request,pk):
    cita=models.idCita.objects.get(idCita=pk)
    cita.status=True
    cita.save()
    return redirect(reverse('asistente_aprobar_cita'))



@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def rechazar_cita_view(request,pk):
    cita=models.Cita.objects.get(id=pk)
    cita.delete()
    return redirect('asistente_aprobar_cita')

@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def eliminar_cita_view(request,pk):
    cita=models.Citas.objects.get(idCita=pk)
    cita.delete()
    return redirect('asistente_ver_citas')



@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def actualizar_cita_view(request,pk):
    cita=models.Citas.objects.get(idCita=pk)
    CitasForm=forms.CitasForm(request.FILES,instance=cita)
    mydict={'CitasForm':CitasForm}
    if request.method=='POST':
        CitasForm=forms.CitasForm(request.POST,request.FILES,instance=cita)
        if CitasForm.is_valid():
            cita=CitasForm.save()
            cita=CitasForm.save(commit=False)
            cita.status=True
            cita.save()
            return redirect('asistente_ver_citas')
    return render(request,'asistente_actualizar_cita.html',context=mydict)

#vista para ver las consultas por cobrar
@login_required(login_url='asistentelogin')
@user_passes_test(is_asistente)
def asistente_citasporcobrar_view(request):
    #citas ejecutadas por cobrar
    citas=models.Citas.objects.all().filter(ejecutada=True, cobrada=False)
    return render(request,'asistente_citasporcobrar.html',{'citas':citas})
#---------------------------------------------------------------------------------
#------------------------ TERMINAN LAS VISTAS DEL ASISTENTE ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------------ COMIENZAN LAS VISTAS DEL MÉDICO ------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='medicologin')
@user_passes_test(is_medico)
def medico_dashboard_view(request):
    #for three cards
    medico = models.Medico.objects.get(user__id=request.user.id)
    medico_id=medico.user.id
    print("el id del medico es:", medico_id)
    print("el nombre del medico es:", medico.user.first_name)
    pacientecount=models.Paciente.objects.all().filter(status=True,medicoAsignadoId=request.user.id).count()
    citascount=models.Citas.objects.all().filter(status=True, medicoId__user__id=medico_id).count()
    cuentapaciente=models.CuentaPaciente.objects.all().distinct().filter(medicoAsignadoNombre=request.user.first_name).count()

    #for  table in doctor dashboard
    fechadehoy=date.today()
    print("la fecha de hoy es: ",fechadehoy)
    citas=models.Citas.objects.all().filter(ejecutada=False, status=True, medicoId__user__id=medico_id,  fechaCita__date=fechadehoy).order_by('-idCita')
    citasdehoy=models.Citas.objects.all().filter(ejecutada=False, status=True, medicoId__user__id=medico_id,  fechaCita__date=fechadehoy).order_by('-idCita').count()
    print("las citas de hoy son:", citasdehoy)

    #para combinar los datos de citas y pacientes
    citas_pacientes = []
    for cita in citas:
        print("este es el ide de la cita", cita.idCita)
        paciente_id = cita.pacienteId.user.id
        nombre_paciente = cita.pacienteId.user.first_name
        print("el nombre del paciente es:", nombre_paciente)
        print("este es el id del paciente de la cita", paciente_id)
        paciente = models.Paciente.objects.filter(user_id=paciente_id, status=True).first()
        pacientesdehoy= models.Paciente.objects.filter(user_id=paciente_id, status=True).count()
        print("hoy tenermos estos pacientes: ", pacientesdehoy)
        if paciente:
            cita_paciente = {
                'idCita': cita.idCita,
                'fechaCita': cita.fechaCita,
                'nombrePaciente': paciente.user.first_name,
                'apellidoPaciente': paciente.user.last_name,
                'telefonoPaciente': paciente.celular,
                'emailPaciente': paciente.user.email,
                'statusCita': cita.status,
                'comentarios': cita.descripcion,
            }
            citas_pacientes.append(cita_paciente)

    mylista={
    'pacientecount':pacientecount,
    'citascount':citascount,
    'cuentapaciente':cuentapaciente,
    'medico':models.Medico.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    'citas_pacientes':citas_pacientes,
    }
    
    #para mostrar los eventos en el calendario
    all_events = Citas.objects.all()
    context = {
        "citas":all_events,
    }
    return render(request,'medico_dashboard.html',context=mylista)

#vista para la ejecución de la consulta
@login_required(login_url='medicologin')
@user_passes_test(is_medico)
def medico_ejecuta_consulta_view(request, pk):
    cita = get_object_or_404(Citas, idCita=pk)
    medico = models.Medico.objects.get(user__id=request.user.id) #para la foto del medico en el sidebar
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.pacienteId = cita.pacienteId
            consulta.medicoId = cita.medicoId
            consulta.idCita = cita
            consulta.save()
            cita.status = True
            cita.ejecutada = True
            cita.save()
            return redirect('medico_dashboard')
    else:
        form = ConsultaForm()
    return render(request, 'medico_ejecuta_consulta.html', {'form': form, 'cita': cita, 'medico':medico})

#vista para que el medico vea todas sus citas
@login_required(login_url='medicologin')
@user_passes_test(is_medico)
def medico_ver_citas_view(request):
    medico = models.Medico.objects.get(user__id=request.user.id)
    medico_id=medico.user.id
    citas=models.Citas.objects.all().filter(status=True, medicoId__user__id=medico_id).order_by('-idCita')
    return render(request,'medico_ver_citas.html',{'citas':citas, 'medico':medico})



#para que el medico pueda eliminar las citas
@login_required(login_url='medicologin')
@user_passes_test(is_medico)
def med_eliminar_cita_view(request,pk):
    cita=models.Citas.objects.get(idCita=pk)
    cita.delete()
    return redirect('medico_dashboard')


#vista para que el medico pueda actualizar sus citas
@login_required(login_url='medicologin')
@user_passes_test(is_medico)
def medico_actualizar_cita_view(request,pk):
    cita=models.Citas.objects.get(idCita=pk)
    CitasForm=forms.CitasForm(request.FILES,instance=cita)
    mydict={'CitasForm':CitasForm}
    if request.method=='POST':
        CitasForm=forms.CitasForm(request.POST,request.FILES,instance=cita)
        if CitasForm.is_valid():
            cita=CitasForm.save()
            cita=CitasForm.save(commit=False)
            cita.status=True
            cita.save()
            return redirect('medico_ver_citas')
    return render(request,'medico_actualizar_cita.html',context=mydict)

#vista para la lista de pacientes que tiene el medico bajo tratamiento
@login_required(login_url='medicologin')
@user_passes_test(is_medico)
def medico_ver_pacientes_view(request):
    medico = models.Medico.objects.get(user__id=request.user.id)
    medico_id=medico.user.id
    pacientes=models.Paciente.objects.all().filter(status=True, medicoAsignadoId=medico_id)
    return render(request,'medico_ver_pacientes.html',{'pacientes':pacientes, 'medico':medico})

@login_required(login_url='medicologin')
@user_passes_test(is_medico)
def medico_utilidades_view(request):
    habitacion_total = 0
    medicamentos_total = 0
    costomedico_total = 0
    otros_total = 0
    #para saber que medico es el que esta logueado
    medico = models.Medico.objects.get(user__id=request.user.id)
    medico_id=medico.user.id
    # Obtener las cuentas de pacientes filtradas
    cuentas=models.CuentaPaciente.objects.all().filter(idCita__medicoId=medico)
    # para obtener los pacientes que ha atendido el medico
    
    
    # Calcular los totales por concepto
    for cuenta in cuentas:
        habitacion_total += cuenta.habitacion
        medicamentos_total += cuenta.medicamenteos
        costomedico_total += cuenta.costomedico
        otros_total += cuenta.otroscargos
    
    # Calcular el gran total
    gran_total = habitacion_total + medicamentos_total + costomedico_total + otros_total

    # Pasar los resultados a la plantilla
    context = {
        'cuentas': cuentas,
        'habitacion_total': habitacion_total,
        'medicamentos_total': medicamentos_total,
        'costomedico_total': costomedico_total,
        'otros_total': otros_total,
        'gran_total': gran_total,
        'medico':medico,
    }

    return render(request, 'medico_utilidades.html', context)
#---------------------------------------------------------------------------------
#------------------------ COMIENZAN LAS VISTAS DEL PACIENTE ----------------------
#---------------------------------------------------------------------------------
@login_required(login_url='pacientelogin')
@user_passes_test(is_paciente)
def paciente_dashboard_view(request):
    paciente=models.Paciente.objects.get(user_id=request.user.id)
    medico=models.Medico.objects.get(user_id=paciente.medicoAsignadoId)
    mylista={
    'paciente':paciente,
    'nombreMedico':medico.get_name,
    'celularMedico':medico.celular,
    'domicilioMedico':medico.domicilio,
    'sintomas':paciente.sintomas,
    'medicoEspecialidad':medico.especialidad,
    'fechadeadmision':paciente.fechadeadmision,
    }
    return render(request,'paciente_dashboard.html',context=mylista)

#---------------------------------------------------------------------------------
#------------------------ COMIENZAN LAS VISTAS DEL CALENDARIO ----------------------
#---------------------------------------------------------------------------------

def calendar(request):
    all_events = Citas.objects.all()
    context = {
        "citas":all_events,
    }
    return render(request,'calendar.html',context)

# para ver los eventos del medico
@login_required(login_url='medicologin')
@user_passes_test(is_medico)
def all_events(request):                                                                                                 
    medico = models.Medico.objects.get(user__id=request.user.id)
    medico_id=medico.user.id
    all_events=models.Citas.objects.all().filter(status=True, medicoId__user__id=medico_id).order_by('-idCita')                                                                                  
    out = []                                                                                                             
    for cita in all_events: 
        title = cita.pacienteNombre
        start = cita.fechaCita
        end = start + timedelta(minutes=30)
        start = start.strftime('%Y-%m-%dT%H:%M:%S')
        end = end.strftime('%Y-%m-%dT%H:%M:%S')                                                                                         
        out.append({                                                                                                     
            'title': title,                                                                                              
            'start': start,                                                         
            'end': end,
        })                                 
    print("esta es para el calendario:", out)                            
    return JsonResponse(out, safe=False)  

# Create event.
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Citas(title=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)

# Update event.
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Citas.objects.get(id=id)
    event.start = start
    event.end = end
    event.title = title
    event.save()
    data = {}
    return JsonResponse(data)

# Remove event.
def remove(request):
    id = request.GET.get("id", None)
    cita = Citas.objects.get(id=id)
    cita.delete()
    data = {}
    return JsonResponse(data)