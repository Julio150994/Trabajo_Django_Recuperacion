from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import RedirectView, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
#Evitamos que cualquier usuario, sin estar logueado, acceda al sistema
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from seguroprivado.models import Paciente, Medico
from seguroprivado.forms import MedicoForm, PacienteForm

# Create your views here.

class RedirectToInicioView(TemplateView):    
    def get(self, request):
        return HttpResponseRedirect('inicio/')

class TemplateInicioView(TemplateView):
    template_name = "seguroprivado/inicio.html"


class RegistroPacientesView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "seguroprivado/registro.html"
    
    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        edad = request.POST.get('edad')
        direccion = request.POST.get('direccion')
        foto = request.FILES.get('foto')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if request.method == "POST":
            if nombre is not None or apellidos is not None or edad is not None or direccion is not None or foto is not None or username is not None or password is not None:
                # Activamos el usuario con el usuario administrador automáticamente
                set_paciente = Paciente(nombre=nombre, apellidos=apellidos, edad=edad, direccion=direccion, foto=foto, activo=True, username=username, password=password)
                set_paciente.password = make_password(set_paciente.password)
                set_paciente.save()
                
                User.objects.create(username=username, password=set_paciente.password)
                return redirect(reverse('login')+"?registered")
            else:
                return redirect('registro')
        else:
            return redirect('registro')
    
class LoginSegPrivadoView(LoginView):
    template_name = "seguroprivado/login.html"

    def get_success_url(self):
        return reverse_lazy('inicio')+'?logged'

    def dispatch(self, request, *args, **kwargs):
        if request.user is not None:
            if request.user.is_active:
                return HttpResponseRedirect('login')
            else:
                if request.user.is_authenticated:
                    return HttpResponseRedirect('inicio')
                else:
                    return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('login')

@method_decorator(login_required, name='dispatch')      
class LogoutView(LoginRequiredMixin, RedirectView):
    pattern_name = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(request,"Ha cerrado sesión.")
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "seguroprivado/perfil_paciente.html"
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('inicio')+'?updated'


@method_decorator(login_required, name='dispatch')
class PacienteList(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "seguroprivado/pacientes.html"

@method_decorator(login_required, name='dispatch')
class PacienteActived(LoginRequiredMixin, UpdateView):
    model = Paciente
    fields = ['activo']
    queryset = Paciente.objects.all()
    success_url = reverse_lazy('pacientes')
       
    def get_context_data(self, **kwargs):
        # Recogemos el objeto de paciente #
        paciente = self.object
        
        # Activamos o desactivamos paciente #
        if paciente.activo == False:
            paciente.activo = True
            messages.add_message(self.request,level=messages.INFO, message="Paciente "+str(paciente.username)+" activado correctamente")
        else:
            paciente.activo = False
            messages.add_message(self.request,level=messages.WARNING, message="Paciente "+str(paciente.username)+" desactivado correctamente")
        paciente.save()
        
  
@method_decorator(login_required, name='dispatch')
class MedicoList(LoginRequiredMixin, ListView):
    model = Medico
    template_name = "seguroprivado/medicos.html"


@method_decorator(login_required, name='dispatch')
class MedicoDetail(LoginRequiredMixin, DetailView):
    model = Medico
    template_name = "seguroprivado/datos_medico.html"

    
@method_decorator(login_required, name='dispatch')
class MedicoCreate(LoginRequiredMixin, CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = "login/form_medico.html"
    success_url = reverse_lazy('medicos')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            nombre = request.POST.get('nombre')
            apellidos = request.POST.get('apellidos')
            edad = request.POST.get('edad')
            fechaalta = request.POST.get('fechaalta')
            especialidad = request.POST.get('especialidad')
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Validamos correctamente la fecha de alta si los datos no son nulos
            if nombre is not None or apellidos is not None or edad is not None or fechaalta is not None or especialidad is not None or username is not None or password is not None:
                anio = str(fechaalta)[0:str(fechaalta).find('-')]# año de alta
                aux_fecha1 = str(fechaalta)[str(fechaalta).find('-')+1:]
                mes = aux_fecha1[0:aux_fecha1.find('-')] # mes de alta
                aux_fecha2 = aux_fecha1[aux_fecha1.find('-')+1:]
                cad_aux = aux_fecha2[0:aux_fecha2.find('-')]
                dia = cad_aux[0:cad_aux.find(' ')]# día de alta
            
                fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
                fecha_alta = datetime(int(anio),int(mes),int(dia))
                
                if fecha_alta <= fecha_actual:
                    set_medico = Medico(nombre=nombre, apellidos=apellidos, edad=edad, fechaalta=fechaalta, especialidad=especialidad, username=username, password=password)
                    set_medico.password = make_password(set_medico.password)
                    set_medico.save()
                
                    # Creamos un usuario médico para iniciar sesión posteriormente
                    User.objects.create(username=username, password=set_medico.password)
                    messages.add_message(request,level=messages.SUCCESS, message="Médico "+str(username)+" añadido correctamente")
                    return redirect('medicos')
                else:
                    messages.add_message(request,level=messages.WARNING, message="La fecha de alta es errónea.")
                    return redirect('form_medico')
                

@method_decorator(login_required, name='dispatch')
class MedicoUpdate(LoginRequiredMixin, UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = "login/form_medico.html"
    success_url = reverse_lazy('medicos')

@method_decorator(login_required, name='dispatch')
class MedicoDelete(LoginRequiredMixin, DeleteView):
    model = Medico
    queryset = Medico.objects.all()
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('medicos')
    
    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            medico = Medico.objects.filter(pk=self.kwargs.get("id"))
            medico.delete()
            
            usuario = User.objects.get(username=medico.username)
            usuario.delete()
            messages.add_message(request,level=messages.ERROR, message="Médico eliminado correctamente")