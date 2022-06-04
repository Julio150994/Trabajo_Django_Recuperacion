"""ProyectoJulio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from seguroprivado import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.RedirectToInicioView.as_view(), name="inicio"),
    path('inicio/',views.TemplateInicioView.as_view(), name="inicio"),
    path('registro/',views.RegistroPacientesView.as_view(),name="registro"),
    path('login/',views.LoginSegPrivadoView.as_view(redirect_authenticated_user=True), name="login"),
    path('logout/',views.LogoutView.as_view(), name="logout"),
    path('perfil_paciente/<slug:username>/', views.EditarPerfilView.as_view(), name="perfil"),
    
    path('pacientes/',views.PacienteList.as_view(), name="pacientes"),
    path('actived/<int:pk>/',views.PacienteActived.as_view(), name="pacientes"),
    
    path('medicos/',views.MedicoList.as_view(), name="medicos"),
    path('aniadir_medico/',views.MedicoCreate.as_view(), name="form_medico"),
    path('editar_medico/<int:pk>/',views.MedicoUpdate.as_view(), name="editar_medico"),
    path('eliminar_medico/<int:pk>/',views.MedicoDelete.as_view(), name="medicos"),
    
    path('medicamentos/',views.MedicamentoList.as_view(), name="medicamentos"),
    path('aniadir_medicamento/',views.MedicamentoCreate.as_view(), name="form_medicamento"),
    path('editar_medicamento/<int:pk>/',views.MedicamentoUpdate.as_view(),name="editar_medicamento"),
    path('eliminar_medicamento/<int:pk>/',views.MedicamentoDelete.as_view(), name="medicamentos"),
    
    path('citas/',views.CitaList.as_view(), name="citas_paciente"),
    path('pedir_cita/',views.CitaCreate.as_view(), name="form_cita"),
    
    path('citas_medico/',views.CitaMedicoList.as_view(), name="citas_medico"),
    path('citas_medico/actuales/',views.CitaActualView.as_view(), name="citas_actuales"),
    path('citas_medico/actuales/<int:pk>/',views.RealizarCitaView.as_view(), name="realizar_citas"),
    path('citas_medico/filtrar/',views.FiltroCitaView.as_view(),name="filtro_citas"),
    
    path('historial_paciente/',views.HistorialPacienteView.as_view(), name="historial_paciente"),
    path('historial_paciente_medico/<int:pk>/',views.HistorialPacientesMedicoView.as_view(), name="historial_pacientes_medico"),
    path('tienda_medicamentos/',views.MedicamentosPacienteView.as_view(), name="tienda"),
    path('compra_medicamento/<int:pk>/', views.CompraMedicamentoView.as_view(), name="compra_medicamento")
    
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
