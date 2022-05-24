from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse_lazy
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
from seguroprivado.models import Cita, Medicamento, Paciente, Medico
from seguroprivado.forms import CitaForm, MedicamentoForm, MedicoForm, PacienteForm
from django.db.models import Q

# Create your views here.

class RedirectToInicioView(TemplateView):    
    def get(self, request):
        return HttpResponseRedirect('inicio/')

class TemplateInicioView(TemplateView):
    template_name = "seguroprivado/inicio.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data()
        contexto['medicos'] = Medico.objects.all()
        
        # Para realizar la búsqueda de médicos por especialidad
        busqueda = self.request.GET.get("especialidad")
        
        if busqueda is not None:
            # Q: revisa todos los campos de un modelo especificado
            # __icontains: es para buscar por especialidad, sin errores por Case Sensitive
            contexto['medicos'] = Medico.objects.filter(Q(especialidad__icontains = busqueda)).distinct()
        return contexto
    
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
            messages.add_message(request, level=messages.SUCCESS, message="Paciente "+str(username)+" registrado correctamente.")
            return redirect('login')
        else:
            messages.add_message(request, level=messages.WARNING, message="Error al registrar paciente")
            return redirect('registro')


class LoginSegPrivadoView(LoginView):
    template_name = "seguroprivado/login.html"
    success_url = reverse_lazy('inicio')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(username=username, password=password)
        
        # Validamos si un usuario está registrado o no en la base de datos
        if User.objects.filter(username=username).exists():
            if usuario is not None:
                # Validamos que el usuario está autenticado
                if usuario.is_authenticated:
                    # Validamos que el usuario sea el administrador
                    if usuario.username == User.objects.get(username="admin").username:
                        login(request,usuario)
                        messages.add_message(request, level=messages.INFO, message=str(username)+" logueado correctamente")
                        return redirect('inicio')
                    else:
                        # Validamos que el usuario es un médico
                        if not Paciente.objects.filter(username=username).exists() and usuario.username == Medico.objects.get(username=username).username:
                            login(request,usuario)
                            messages.add_message(request, level=messages.INFO, message="Médico "+str(username)+" logueado correctamente")
                            return redirect('inicio')
                        # Validamos que el usuario es un paciente
                        else:
                            usuario_paciente = Paciente.objects.get(username=username)
                            # Validamos de que el paciente esté activado
                            if usuario_paciente.activo == True:
                                login(request,usuario)
                                messages.add_message(request, level=messages.INFO, message="Paciente "+str(username)+" logueado correctamente")                                
                                return redirect('inicio')
                            else:
                                messages.add_message(request, level=messages.WARNING, message="El paciente "+str(username)+" no está activado")
                                return redirect('login')
            else:
                messages.add_message(request, level=messages.WARNING, message="Credenciales de "+str(username)+" erróneas.")
                return redirect('login')
        else:
            messages.add_message(request, level=messages.WARNING, message="El usuario "+str(username)+" no existe.")
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
    slug_field = "username" # nombre del campo de tabla pacientes
    slug_url_kwarg = "username" # nombre del argumento que pasamos en urls.py
    success_url = reverse_lazy('inicio')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):        
        get_paciente = self.get_object()
        paciente = PacienteForm(request.POST)
        
        if paciente.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            set_paciente = paciente.save(commit=False)
            set_paciente.password = make_password(password)
            set_paciente.save()
            
            usuario = User.objects.get(username=username)
            usuario.delete()
            
            set_paciente = User.objects.create(username=username, password=set_paciente.password)
            set_paciente.save()   
        
        messages.add_message(request,level=messages.INFO, message="Perfil de paciente "+str(get_paciente.username)+" editado correctamente")
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

      
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class MedicamentoList(LoginRequiredMixin, ListView):
    model = Medicamento
    template_name = "seguroprivado/medicamentos.html"


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class MedicamentoCreate(LoginRequiredMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = "seguroprivado/form_medicamento.html"
    success_url = reverse_lazy('medicamentos')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        medicamento = MedicamentoForm(request.POST)
        
        if medicamento.is_valid():
            nombre = request.POST.get("nombre")
            messages.add_message(request,level=messages.SUCCESS, message="Medicamento "+str(nombre)+" añadido correctamente")
            return super().post(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class MedicamentoUpdate(LoginRequiredMixin, UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = "seguroprivado/editar_medicamento.html"
    success_url = reverse_lazy('medicamentos')
    
    def dispatch(self, request, *args, **kwargs):        
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        medicamento_anterior = self.get_object()# recibimos el medicamento anterior
        medicamento = MedicamentoForm(request.POST)
        
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        receta = request.POST.get("receta")
        precio = request.POST.get("precio")
        stock = request.POST.get("stock")
        
        medicamento_actual = Medicamento.objects.get(id=medicamento_anterior.id)
        medicamento_actual.nombre = nombre
        medicamento_actual.descripcion = descripcion
        medicamento_actual.receta = receta
        medicamento_actual.precio = float(precio)
        medicamento_actual.stock += int(stock)
        
        if medicamento_actual.nombre == medicamento_anterior.nombre:
            messages.add_message(request,level=messages.WARNING, message="Debe cambiar el nombre del medicamento "+str(medicamento_anterior.nombre))
        else:                        
            medicamento_actual.save()
            messages.add_message(request,level=messages.INFO, message="Medicamento "+str(nombre)+" editado correctamente")
        return redirect(self.success_url)
        
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: user.is_superuser), name='dispatch')# Administrador
class MedicamentoDelete(LoginRequiredMixin, DeleteView):
    model = Medicamento
    queryset = Medicamento.objects.all()
    success_url = reverse_lazy('medicamentos')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def render_to_response(self, context, **response_kwargs):
        obj_medicamento = self.get_object()
        
        if obj_medicamento is not None:            
            medicamento = Medicamento.objects.filter(id=obj_medicamento.id)
            medicamento.delete()
            
            messages.add_message(self.request,level=messages.WARNING, message="Medicamento "+str(obj_medicamento.nombre)+" eliminado correctamente")
            return redirect('medicamentos')


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and not user.is_staff), name='dispatch')# Paciente
class CitaList(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "seguroprivado/citas_paciente.html"

    def get_context_data(self, **kwargs):
        context = super(CitaList, self).get_context_data(**kwargs)
        
        paciente = Paciente.objects.get(username=self.request.user)
        # Buscamos si el paciente tiene o no citas pendientes
        citas_paciente = Cita.objects.filter(idPaciente=paciente)
        context['citas_paciente'] = citas_paciente
        
        fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day)) 
        print("Fecha actual: "+str(fecha_actual))
        aux_cita = ""
        
        fechas = Cita.objects.all().values_list('fecha')
        for cita in fechas:
            for item in cita:
                fecha_cita = datetime.strptime(str(item),'%Y-%m-%d')
                
                if fecha_cita == fecha_actual:
                    context['citas_pendientes'] = aux_cita
        
        context['citas_pendientes']
        return context
    

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and not user.is_staff), name='dispatch')# Paciente
class CitaCreate(LoginRequiredMixin, CreateView):
    model = Cita
    form_class = CitaForm
    template_name = "seguroprivado/form_cita.html"
    success_url = reverse_lazy('citas_paciente')
    error_url = reverse_lazy('form_cita')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        paciente = Paciente.objects.get(username=self.request.user)
        
        context = {}
        dict_pacientes = {"idPaciente": paciente}
        
        form = CitaForm(self.request.POST, initial=dict_pacientes)
        context['form'] = form
        return super().get_context_data()
    
    def post(self, request, *args, **kwargs):
        form = CitaForm(request.POST)
        
        dict_citas = dict()
        nueva_cita = dict()
        lista_citas = list()
        list_aux_medico = list()
        
        # Obtenemos el objeto del paciente
        idPaciente = request.POST.get('idPaciente')
        paciente = Paciente.objects.get(id=idPaciente).username
        
        # Obtenemos el objeto del médico
        idMedico = request.POST.get('idMedico')
        medico = Medico.objects.get(id=idMedico)
        
        fecha = request.POST.get('fecha')# fecha de cita enviada
        fecha_cita = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
        
        if fecha_cita < fecha_actual:
            messages.add_message(request, level=messages.WARNING, message="La fecha de cita debe ser mayor o igual que la fecha actual")
            return redirect(self.error_url)
        else:
            for cita in Cita.objects.all().order_by('-id'):
                dict_citas = {str(cita.idMedico.username): str(cita.fecha)}
                lista_citas.append(dict_citas)
        
            nueva_cita.update({str(medico.username): str(fecha)})
            lista_citas.append(nueva_cita)
            
            for item in lista_citas:
                contador = lista_citas.count(item)
                list_aux_medico.append(contador)
            
            citas_repetidas = lista_citas.count({str(medico.username) : str(fecha)})
            
            # Validamos que un médico solamente puede atender hasta 3 citas en un mismo día.
            if citas_repetidas == 3:
                # Convertimos la fecha del formato yyyy-mm-dd al formato dd/mm/YYYY
                anio = str(fecha)[0:str(fecha).find('-')]
                aux = str(fecha)[str(fecha).find('-')+1:]
                mes = aux[0:str(aux).find('-')]
                dia = aux[str(aux).find('-')+1:]
                
                fecha_repetida = str(dia)+"/"+str(mes)+"/"+str(anio)
                messages.add_message(request, level=messages.WARNING, message="El médico "+str(medico.username)+" no puede atender más citas para el "+str(fecha_repetida))
                return redirect(self.error_url)
            else:
                if form.is_valid():       
                    messages.add_message(request, level=messages.SUCCESS, message="Cita para "+str(paciente)+" añadida correctamente")
                    return super().post(request, *args, **kwargs)