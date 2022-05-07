from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import RedirectView, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
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


@method_decorator(login_required, name='dispatch')
class PacienteList(ListView):
    model = Paciente
    template_name = "seguroprivado/pacientes.html"
    
class PacienteActived(UpdateView):
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
class MedicoList(ListView):
    model = Medico
    template_name = "seguroprivado/medicos.html"


@method_decorator(login_required, name='dispatch')
class MedicoDetail(DetailView):
    model = Medico
    template_name = "seguroprivado/datos_medico.html"

    
@method_decorator(login_required, name='dispatch')
class MedicoCreate(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = "login/form_medico.html"
    success_url = reverse_lazy('medicos')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):        
        medico = form['medico'].save(commit=False)
        
        anio = str(medico.fechaalta)[0:str(medico.fechaalta).find('-')]# año de alta
        aux_fecha1 = str(medico.fechaalta)[str(medico.fechaalta).find('-')+1:]
        mes = aux_fecha1[0:aux_fecha1.find('-')] # mes de alta
        aux_fecha2 = aux_fecha1[aux_fecha1.find('-')+1:]
        cad_aux = aux_fecha2[0:aux_fecha2.find('-')]
        dia = cad_aux[0:cad_aux.find(' ')]# día de alta
        
        fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
        fecha_alta = datetime(int(anio),int(mes),int(dia))
        
        if fecha_alta <= fecha_actual:
            medico.password = make_password(medico.password)
            
            usuario = User.objects.create(username=medico.username, password=medico.password)
            medico.usuario = usuario
            medico.save()
            messages.add_message(self.request, level=messages.SUCCESS, message="Médico "+str(medico.username)+" añadido correctamente.")
            return HttpResponseRedirect('medicos')
   
@method_decorator(login_required, name='dispatch')
class MedicoDelete(DeleteView):
    model = Medico
    
    def get_success_url(self):
        return reverse_lazy('medicos')+"?deleted"
    