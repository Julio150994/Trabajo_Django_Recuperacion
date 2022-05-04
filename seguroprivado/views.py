from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import RedirectView, TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from seguroprivado.models import Paciente
from seguroprivado.forms import PacienteForm

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
class LogoutView(RedirectView):
    pattern_name = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(request,"Ha cerrado sesión.")
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class EditarPerfilView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "seguroprivado/perfil_paciente.html"
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('inicio')+'?updated'