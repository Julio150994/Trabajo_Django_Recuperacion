from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import RedirectView, TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
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
    
    def get_success_url(self):
        return reverse_lazy('login')+'?registered'
    
class LoginSegPrivadoView(LoginView):
    template_name = "seguroprivado/login.html"

    def get_success_url(self):
        return reverse_lazy('inicio')+'?logged'

    def dispatch(self, request, *args, **kwargs):
        if request.user is not None:
            if request.user.is_active:
                #messages.error(request, 'Este usuario ya está logueado')
                return HttpResponseRedirect('login')
            else:
                if request.user.is_authenticated:
                    return HttpResponseRedirect('inicio')
                else:
                    #messages.error(request, 'Credenciales de usuario erróneas')
                    return super().dispatch(request, *args, **kwargs)
        else:
            #messages.error(request, 'Este usuario ya está registrado')
            return HttpResponseRedirect('login')
        
class LogoutView(RedirectView):
    pattern_name = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        messages.success(request,"Ha cerrado sesión.")
        return super().dispatch(request, *args, **kwargs)
    
class EditarPerfilView(UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "seguroprivado/perfil_paciente.html"
    
    def get_success_url(self):
        return reverse_lazy('inicio')+'?updated'