from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import RedirectView, TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
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
            # Activamos el usuario con el usuario administrador automáticamente
            set_paciente = Paciente(nombre=nombre, apellidos=apellidos, edad=edad, direccion=direccion, foto=foto, activo=True, username=username, password=password)
            set_paciente.password = make_password(set_paciente.password)
            set_paciente.save()
            
            User.objects.create(username=username, password=set_paciente.password)
            return redirect(reverse('login')+"?registered")
        else:
            messages.add_message(self.request, level=messages.WARNING, message="Error al registrar paciente")
            return redirect('registro')


class LoginSegPrivadoView(LoginView):
    template_name = "seguroprivado/login.html"

    def get_success_url(self):
        #'?logged'#
        return reverse_lazy('inicio')

    # Validamos la conexión de los usuarios
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(username=username, password=password)

        if usuario is not None:
            if usuario.is_authenticated:
                login(request,usuario)
                messages.add_message(request, level=messages.INFO, message="Usuario "+str(request.user)+" logueado correctamente")
                return redirect('inicio')
        else:
            messages.add_message(request, level=messages.WARNING, message="Error en las credenciales")
            return redirect('login')

# Decoradores para dar permiso a los usuarios
@method_decorator(login_required, name='dispatch')
class LogoutView(RedirectView):
    pattern_name = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        username = request.user.username
        logout(request)
        messages.info(request, str(username)+" ha cerrado sesión.")
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and not user.is_staff), name='dispatch')# Paciente
class EditarPerfilView(LoginRequiredMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm
    template_name = "seguroprivado/perfil_paciente.html"
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('inicio')+'?updated'
    

    def post(self, request, *args, **kwargs):        
        obj_paciente = self.get_object()# nos ayuda a obtener el id del médico a editar
        datos_paciente = Paciente.objects.get(pk=obj_paciente.id)
        paciente = PacienteForm(request.POST, instance=datos_paciente)
        
        if paciente.is_valid():
            set_paciente = paciente.save(commit=False)
            set_paciente.password = make_password(set_paciente.password)
            set_paciente.save()
            
            usuario = User.objects.get(username=obj_paciente.username)
            usuario.delete()
            
            set_paciente = User.objects.create(username=obj_paciente.username, password=set_paciente.password)
            set_paciente.save()
        
        return super().post(request, *args, **kwargs)  
    

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class PacienteList(LoginRequiredMixin, ListView):
    model = Paciente
    template_name = "seguroprivado/pacientes.html"

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class PacienteActived(LoginRequiredMixin, UpdateView):
    model = Paciente
    fields = ['activo']
    queryset = Paciente.objects.all()
    success_url = reverse_lazy('pacientes')
       
    def get_context_data(self, **kwargs):
        paciente = self.get_object()# recogemos el objeto de paciente
        
        if paciente.activo == False:
            paciente.activo = True
            messages.add_message(self.request,level=messages.INFO, message="Paciente "+str(paciente.username)+" activado correctamente")
        else:
            paciente.activo = False
            messages.add_message(self.request,level=messages.WARNING, message="Paciente "+str(paciente.username)+" desactivado correctamente")
        paciente.save()

    def render_to_response(self, context, **response_kwargs):
        # Método para redireccionar a la misma página
        paciente = self.get_object()
        
        if paciente is not None:
            return redirect('pacientes')
  
  
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class MedicoList(LoginRequiredMixin, ListView):
    model = Medico
    template_name = "seguroprivado/medicos.html"


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class MedicoCreate(LoginRequiredMixin, CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = "seguroprivado/form_medico.html"
    
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
               
            # Validación de la fecha de alta
            fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
            fecha_alta = datetime.strptime(fechaalta, '%Y-%m-%d')
            
            if fecha_alta <= fecha_actual:
                set_medico = Medico(nombre=nombre, apellidos=apellidos, edad=edad, fechaalta=fechaalta, especialidad=especialidad, username=username, password=password)
                set_medico.password = make_password(set_medico.password)
                set_medico.save()
            
                # Autogeneramos un usuario médico para iniciar sesión posteriormente
                set_medico = User.objects.create(username=username, password=set_medico.password)
                set_medico.is_staff = True
                set_medico.save()
                
                messages.add_message(request,level=messages.SUCCESS, message="Médico "+str(username)+" añadido correctamente")
                return redirect('medicos')
            else:
                messages.add_message(request,level=messages.WARNING, message="La fecha de alta es errónea.")
                return redirect('form_medico')


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class MedicoUpdate(LoginRequiredMixin, UpdateView):
    model = Medico
    form_class = MedicoForm
    template_name = "seguroprivado/editar_medico.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        get_medico = self.get_object()# nos ayuda a obtener el id del médico a editar
        datos_medico = Medico.objects.get(pk=get_medico.id)
        medico = MedicoForm(request.POST, instance=datos_medico)
        
        if medico.is_valid():
            fechaalta = request.POST.get('fechaalta')
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            # Validación de la fecha de alta
            fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
            fecha_alta = datetime.strptime(fechaalta, '%Y-%m-%d')
            
            if fecha_alta <= fecha_actual:
                # Editamos nuestro usuario #
                set_medico = medico.save(commit=False)
                set_medico.password = make_password(password)
                set_medico.save()
                
                usuario = User.objects.get(username=get_medico.username)
                usuario.delete()
                
                set_medico = User.objects.create(username=username, password=set_medico.password)
                set_medico.is_staff = True
                set_medico.save()
                
                messages.add_message(request,level=messages.INFO, message="Médico "+str(username)+" editado correctamente.")
                return redirect('medicos')
            else:
                messages.add_message(request,level=messages.WARNING, message="La fecha de alta es errónea.")
                return redirect('editar_medico/'+str(get_medico.id)+'/')    
    
    
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class MedicoDelete(LoginRequiredMixin, DeleteView):
    model = Medico
    queryset = Medico.objects.all()
    success_url = reverse_lazy('medicos')
    
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def render_to_response(self, context, **response_kwargs):
        # Método para redireccionar a la misma página
        obj_medico = self.get_object()
        
        if obj_medico is not None:
            medico = Medico.objects.filter(id=obj_medico.id)
            medico.delete()
            
            usuario = User.objects.get(username=obj_medico.username)
            usuario.delete()
            
            messages.add_message(self.request,level=messages.WARNING, message="Médico "+str(obj_medico.username)+" eliminado correctamente")
            return redirect('medicos')