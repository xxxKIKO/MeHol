"""
URL configuration for prueba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from consultas import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    #inicio y admin
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),

    #sobre nosotros y contactanos
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

    #asistente, medico y paciente click
    path('asistenteclick', views.asistenteclick),
    path('medicoclick', views.medicoclick),
    path('pacienteclick', views.pacienteclick),

    #registro de asistente, médico y pacinte
    path('asistentesignup', views.asistentesignup),
    path('medicosignup', views.medicosignup,name='medicosignup'),
    path('pacientesignup', views.pacientesignup),
    
    #login de asistente, médico y paciente
    path('asistentelogin', LoginView.as_view(template_name='asistentelogin.html')),
    path('medicologin', LoginView.as_view(template_name='medicologin.html')),
    path('pacientelogin', LoginView.as_view(template_name='pacientelogin.html')),

    #depués de login y logout
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='index.html'),name='logout'),

    #todas las urls del asistente
    #primero las que son para manejar al medico
    path('asistente_dashboard', views.asistente_dashboard_view,name='asistente_dashboard'),
    path('asistente_menu_medicos', views.asistente_medicos_view,name='asistente_menu_medicos'),
    path('asistente_aprobar_medico', views.asistente_aprobar_medico_view,name='asistente_aprobar_medico'),
    path('aprobar_medico/<int:pk>', views.aprobar_medico_view,name='aprobar_medico'),
    path('rechazar_medico/<int:pk>', views.rechazar_medico_view,name='rechazar_medico'),
    path('asistente_agregar_medico', views.asistente_agregar_medico_view,name='asistente_agregar_medico'),
    path('asistente_lista_medicos', views.asistente_lista_medicos_view,name='asistente_lista_medicos'),
    path('eliminar_medico/<int:pk>', views.eliminar_medico_view,name='eliminar_medico'),
    path('actualizar_medico/<int:pk>', views.actualizar_medico_view,name='actualizar_medico'),
    path('asistente_medico_especialidad',views.asistente_medico_especialidad_view,name='asistente_medico_especialidad'),
    #luego las que son para manejar al paciente
    path('asistente_menu_pacientes', views.asistente_menu_pacientes_view,name='asistente_menu_pacientes'),
    path('asistente_aprobar_paciente', views.asistente_aprobar_paciente_view,name='asistente_aprobar_paciente'),
    path('aprobar_paciente/<int:pk>', views.aprobar_paciente_view,name='aprobar_paciente'),
    path('rechazar_paciente/<int:pk>', views.rechazar_paciente_view,name='rechazar_paciente'),
    path('asistente_agregar_paciente', views.asistente_agregar_paciente_view,name='asistente_agregar_paciente'),
    path('asistente_lista_pacientes', views.asistente_lista_pacientes_view,name='asistente_lista_pacientes'),
    path('eliminar_paciente/<int:pk>', views.eliminar_paciente_view,name='eliminar_paciente'),
    path('actualizar_paciente/<int:pk>', views.actualizar_paciente_view,name='actualizar_paciente'),
    path('asistente_alta_paciente', views.asistente_alta_paciente_view,name='asistente_alta_paciente'),
    path('alta_paciente/<int:pk>', views.alta_paciente_view,name='alta_paciente'),
    path('paciente_descarga_cuenta/<int:pk>', views.paciente_descarga_cuenta_view,name='paciente_descarga_cuenta'),

    #aqui van las vistas para las citas
    path('asistente_menu_citas', views.asistente_menu_citas_view,name='asistente_menu_citas'),
    path('asistente_ver_citas', views.asistente_ver_citas_view,name='asistente_ver_citas'),
    path('asistente_agregar_citas', views.asistente_agregar_citas_view,name='asistente_agregar_citas'),
    path('asistente_aprobar_citas', views.asistente_aprobar_citas_view,name='asistente_aprobar_citas'),
    path('aprobar_cita/<int:pk>', views.aprobar_cita_view,name='aprobar_cita'),
    path('rechazar_cita/<int:pk>', views.rechazar_cita_view,name='rechazar_cita'),
    path('eliminar_cita/<int:pk>', views.eliminar_cita_view,name='eliminar_cita'),
    path('actualizar_cita/<int:pk>', views.actualizar_cita_view,name='actualizar_cita'),
    path('asistente_citasporcobrar', views.asistente_citasporcobrar_view,name='asistente_citasporcobrar'),
    path('asistente_cobrar_cita/<int:pk>', views.asistente_cobrar_cita_view,name='asistente_cobrar_cita'),
    path('asistente_descarga_cobro/<int:pk>', views.asistente_descarga_cobro_view,name='asistente_descarga_cobro'),

    #todas las urls del médico
    path('medico_dashboard', views.medico_dashboard_view,name='medico_dashboard'),
    path('med_eliminar_cita/<int:pk>', views.med_eliminar_cita_view,name='med_eliminar_cita'),
    path('medico_ejecuta_consulta/<int:pk>', views.medico_ejecuta_consulta_view,name='medico_ejecuta_consulta'),
    path('medico_ver_citas', views.medico_ver_citas_view,name='medico_ver_citas'),
    path('medico_actualizar_cita/<int:pk>', views.medico_actualizar_cita_view,name='medico_actualizar_cita'),
    path('medico_ver_pacientes', views.medico_ver_pacientes_view,name='medico_ver_pacientes'),
        #todas las vistas para el calendario
    path('all_events', views.all_events, name='all_events'),

    #todas las urls del paciente
    path('paciente_dashboard', views.paciente_dashboard_view,name='paciente_dashboard'),


]
