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
    path('login/',views.LoginSegPrivadoView.as_view(), name="login"),
    path('logout/',views.LogoutView.as_view(), name="logout"),
    path('perfil_paciente/<int:pk>/', views.EditarPerfilView.as_view(), name="perfil"),
    
    path('pacientes/',views.PacienteList.as_view(), name="pacientes"),
    path('actived/<int:pk>/',views.PacienteActivedView.as_view(), name="pacientes"),
    
    path('medicos/',views.MedicoList.as_view(), name="medicos"),
    path('medico/<int:pk>/',views.MedicoDetail.as_view(), name="datos_medico"),
    path('aniadir_medico/',views.MedicoCreate.as_view(), name="form_medico"),
    path('eliminar_medico/<int:pk>/',views.MedicoDelete.as_view(), name="delete"),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
