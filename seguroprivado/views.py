from datetime import datetime
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import RedirectView, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from seguroprivado.models import Cita, CompraMedicamento, Compra, Medicamento, Paciente, Medico
from seguroprivado.forms import CitaForm, MedicamentoForm, MedicoForm, PacienteForm
from django.db.models import Q
from seguroprivado.carrito import CarritoCompra # reutilizamos la clase con las funciones del carrito

# Create your views here.

class RedirectToInicioView(TemplateView):    
    def get(self, request):
        return HttpResponseRedirect('inicio/')

class TemplateInicioView(TemplateView):
    template_name = "seguroprivado/inicio.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        medicos = Medico.objects.all()
        context['medicos'] = medicos
        
        if medicos.exists():
            busqueda = self.request.GET.get("especialidad")
            
            if busqueda is None:
                context['especialidad'] = medicos
            else:
                # Q: revisa todos los campos de un modelo especificado
                # __icontains: es para buscar por especialidad, sin errores por Case Sensitive
                consulta_especialidad = Medico.objects.filter(
                    Q(especialidad__icontains = busqueda)
                ).distinct()
                
                if consulta_especialidad.exists():
                    context['especialidad'] = consulta_especialidad
                else:
                    context['nombre_especialidad'] = busqueda
        
        # Para poder acceder al historial de los pacientes del médico
        pacientes = Paciente.objects.all()            
        context['pacientes'] = pacientes
        return context
    
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
        medicamento_actual.stock += int(stock) # para aumentar el stock
        
        messages.add_message(request, level=messages.INFO, message="Medicamento "+str(nombre)+" editado correctamente")
        medicamento_actual.save()
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
        

# Mostrar citas del paciente
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and not user.is_staff), name='dispatch')# Paciente
class CitaList(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "seguroprivado/citas_paciente.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CitaList, self).get_context_data(**kwargs)
        
        paciente = Paciente.objects.get(username=self.request.user)
        citas_paciente = Cita.objects.filter(idPaciente=paciente)
        context['citas_paciente'] = citas_paciente    
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
    
    def post(self, request, *args, **kwargs):
        form = CitaForm(request.POST)
        
        dict_citas = dict()
        nueva_cita = dict()
        lista_citas = list()
        list_aux_medico = list()
        
        # Obtenemos al paciente logueado
        paciente = Paciente.objects.get(username=self.request.user)
        
        # Obtenemos el objeto del médico
        idMedico = request.POST.get('idMedico')
        medico = Medico.objects.get(id=idMedico)
        
        fecha = request.POST.get('fecha')# fecha de cita enviada)
        fecha_cita = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
        
        tratamiento = request.POST.get('tratamiento')
        observaciones = request.POST.get('observaciones')# fecha de cita enviada
        
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
            if citas_repetidas > 3:
                # Convertimos la fecha del formato yyyy-mm-dd al formato dd/mm/YYYY
                anio = str(fecha)[0:str(fecha).find('-')]
                aux = str(fecha)[str(fecha).find('-')+1:]
                mes = aux[0:str(aux).find('-')]
                dia = aux[str(aux).find('-')+1:]
                
                fecha_repetida = str(dia)+"/"+str(mes)+"/"+str(anio)
                messages.add_message(request, level=messages.WARNING, message="El médico "+str(medico.username)+" no puede atender más citas para el "+str(fecha_repetida))
                return redirect(self.error_url)
            else:
                # Pedimos la cita para el paciente logueado
                cita = Cita(idPaciente=paciente, idMedico=medico, fecha=fecha, tratamiento=tratamiento, observaciones=observaciones, realizada=False)
                cita.save()
                messages.add_message(request, level=messages.SUCCESS, message="Su cita ha sido añadida correctamente")
                return redirect(self.success_url)

# Clases para que los médicos puedan realizar sus consultas
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and user.is_staff), name='dispatch')# Médico
class CitaMedicoList(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "seguroprivado/citas_medico.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CitaMedicoList, self).get_context_data(**kwargs)
        
        # Mostramos las citas del médico actual
        medico = Medico.objects.get(username=self.request.user)
        # Buscamos si el médico tiene pacientes en sus citas
        citas_medico = Cita.objects.filter(idMedico=medico)
        context['citas_medico'] = citas_medico
        
        if citas_medico.exists():
            context['filtro_fechas'] = citas_medico
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and user.is_staff), name='dispatch')# Médico
class CitaActualView(CitaMedicoList): # utilización de herencia de clase
    template_name = "seguroprivado/citas_actuales.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CitaActualView, self).get_context_data(**kwargs)
        
        medico = Medico.objects.get(username=self.request.user)
        fecha_actual = datetime(int(datetime.today().year),int(datetime.today().month),int(datetime.today().day))
        formato_fecha_actual = datetime.strftime(fecha_actual,'%Y-%m-%d')
        
        citas_fecha_actual = Cita.objects.filter(idMedico=medico).filter(fecha=str(formato_fecha_actual))
        context['fecha_actual'] = formato_fecha_actual
        context['citas_hoy'] = citas_fecha_actual
        
        # Para el select de medicamentos
        context['medicamentos'] = Medicamento.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and user.is_staff), name='dispatch')# Médico
class RealizarCitaView(LoginRequiredMixin, UpdateView):
    model = Cita
    success_url = reverse_lazy('citas_actuales')
    
    def dispatch(self, request, *args, **kwargs):    
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        paciente_cita = self.get_object() # para obtener el paciente al cual se le realiza la cita
        
        id_tratamiento = request.POST.get("tratamiento")
        aux_id = int(id_tratamiento)
        set_medicamento = Medicamento.objects.get(id=aux_id) 
        
        if paciente_cita.realizada == False:
            paciente_cita.tratamiento = set_medicamento.nombre
            paciente_cita.realizada = True
            paciente_cita.save()
            messages.add_message(self.request,level=messages.INFO, message="Cita de "+str(paciente_cita.idPaciente.username)+" realizada correctamente")
            return redirect(self.success_url)

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and user.is_staff), name='dispatch')# Médico
class FiltroCitaView(LoginRequiredMixin, TemplateView):
    template_name = "seguroprivado/filtro_citas.html"
    success_url = reverse_lazy('citas_medico')
    error_url = reverse_lazy('filtro_citas')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        medico = Medico.objects.get(username=request.user)# médico logueado obtenido
                
        fecha_inicio = request.GET.get("fecha_inicio")
        fecha_final = request.GET.get("fecha_final")
        
        if fecha_inicio is not None and fecha_final is not None:
            inicio = datetime.strptime(str(fecha_inicio),"%Y-%m-%d")
            final = datetime.strptime(str(fecha_final),"%Y-%m-%d")
            
            formato_fecha_inicio = datetime.strptime(str(fecha_inicio),'%Y-%m-%d')
            formato_fecha_final = datetime.strptime(str(fecha_final),'%Y-%m-%d')
            
            if formato_fecha_inicio > formato_fecha_final:
                messages.add_message(request, level=messages.WARNING, message="La fecha inicial no puede ser mayor que la fecha final")
                return redirect(self.error_url)
            else:
                citas_medico = Cita.objects.filter(idMedico=medico)
                context['citas_medico'] = citas_medico # llevamos la consulta a la tabla de citas del médico
                
                if citas_medico.exists():                    
                    filtro = Cita.objects.filter(idMedico=medico).filter(fecha__range=(formato_fecha_inicio, formato_fecha_final))
                    context['filtro_fechas'] = filtro
                    
                    if not filtro.exists():
                        # Mostramos el error de validación cuando no hay citas entre ese rango de fechas y con el formato dd/mm/yyyy
                        aux_fecha_inicio = datetime.strptime(str(inicio),"%Y-%m-%d %H:%M:%S")
                        aux_fecha_final = datetime.strptime(str(final),"%Y-%m-%d %H:%M:%S")
                        mensaje_fecha_inicio = aux_fecha_inicio.strftime("%d/%m/%Y")
                        mensaje_fecha_final = aux_fecha_final.strftime("%d/%m/%Y")
                        
                        context['fecha_inicio'] = mensaje_fecha_inicio
                        context['fecha_final'] = mensaje_fecha_final
                        
                return render(request, "seguroprivado/citas_medico.html", context)
        return super().get(request, *args, **kwargs)   

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and not user.is_staff), name='dispatch')# Paciente
class HistorialPacienteView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = "seguroprivado/historial_paciente.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(HistorialPacienteView, self).get_context_data(**kwargs)
        
        fecha_actual = datetime(int(datetime.today().year),int(datetime.today().month),int(datetime.today().day))
        formato_fecha_actual = datetime.strftime(fecha_actual,'%Y-%m-%d')
        
        paciente = Paciente.objects.get(username=self.request.user)
        historial = Cita.objects.filter(idPaciente=paciente).filter(fecha__lte=formato_fecha_actual).order_by('-fecha')
        
        context['historial_citas'] = historial
        
        if historial.exists():
            # Filtramos por fecha de citas anteriores del paciente actual
            fecha_cita_anterior = self.request.GET.get("fecha")
            
            if fecha_cita_anterior is None:
                context['fecha_historial'] = historial
            else:
                aux_fecha_cita = datetime.strptime(str(fecha_cita_anterior),"%d/%m/%Y")
                fecha = aux_fecha_cita.strftime('%Y-%m-%d')
                
                filtrar_fecha = Cita.objects.filter(
                    Q(fecha__icontains = fecha)
                ).distinct()
                
                if filtrar_fecha.exists():
                    context['fecha_historial'] = filtrar_fecha
                else:
                    context['fecha_anterior'] = fecha_cita_anterior
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and user.is_staff), name='dispatch')# Médico
class HistorialPacientesMedicoView(LoginRequiredMixin, DetailView):
    model = Paciente
    template_name = "seguroprivado/historial_paciente_medico.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(HistorialPacientesMedicoView, self).get_context_data(**kwargs)        
        paciente = self.get_object()
        
        context['nombre_usuario_paciente'] = paciente.username # mostramos el nombre del paciente obtenido
        
        # Mostramos las citas anteriores que tiene el médico
        medico = Medico.objects.get(username=self.request.user)
        
        # Buscamos si el médico tiene pacientes en sus citas anteriores
        fecha_actual = datetime(int(datetime.today().year),int(datetime.today().month),int(datetime.today().day))
        formato_fecha_actual = datetime.strftime(fecha_actual,'%Y-%m-%d')
        
        historial_medico = Cita.objects.filter(idMedico=medico).filter(idPaciente=paciente).filter(fecha__lte=formato_fecha_actual).order_by('-fecha')
        context['historial_pacientes_medico'] = historial_medico
        return context

# Clases para la parte del carrito de la compra simulado
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and not user.is_staff), name='dispatch')# Paciente
class MedicamentosPacienteView(LoginRequiredMixin, ListView):
    model = CompraMedicamento
    template_name = "seguroprivado/tienda_medicamentos.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MedicamentosPacienteView, self).get_context_data(**kwargs)
        medicamentos = Medicamento.objects.all().order_by('id')
        context['medicamentos'] = medicamentos
        
        paciente_logueado = Paciente.objects.get(username=self.request.user)
        context['paciente_actual'] = paciente_logueado
        
        compra_paciente = Compra.objects.filter(idPaciente=paciente_logueado).all()
        precios_compra = list()
        lista_compras = list()
        lista_medicamentos = list()
        
        for compra in compra_paciente:
            precios_compra.append(compra.precio)
        
        context['precio_total'] = round(sum(precios_compra),2)
        medicamentos_paciente = CompraMedicamento.objects.all()
        medicamentos = Medicamento.objects.all()
        
        # Almacenamos en una lista todos los medicamentos y en otra
        # los que han comprado los pacientes
        for compra in medicamentos_paciente:
            lista_compras.append(compra.idMedicamento.nombre)
        
        for medicamento in medicamentos:
            lista_medicamentos.append(medicamento)
        
        # Validamos los medicamentos que han sido comprados por el paciente
        aux_compras = list(set(medicamentos).intersection(set(medicamentos_paciente)))
          
        context['medicamentos_comprados'] = aux_compras
        context['medicamentos_paciente'] = medicamentos_paciente
        return context

@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and not user.is_staff), name='dispatch')# Paciente
class CompraMedicamentoView(LoginRequiredMixin, CreateView):
    model = Medicamento
    success_url = reverse_lazy('tienda')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CompraMedicamentoView, self).get_context_data(**kwargs)                
        context['medicamentos'] = Medicamento.objects.all().order_by('id')          
        return context
    
    def post(self, request, *args, **kwargs):        
        nombre_medicamento = self.get_object()# para obtener el medicamento agregado a la compra
        carrito = CarritoCompra
        
        # Obtenemos el paciente actual
        paciente_compra = Paciente.objects.get(username=self.request.user)
        
        # Agregamos la compra del medicamento        
        medicamento = Medicamento.objects.get(nombre=nombre_medicamento)
        
        fecha_actual = datetime(int(datetime.today().year),int(datetime.today().month),int(datetime.today().day))
        fecha_compra = datetime.strftime(fecha_actual,'%Y-%m-%d')
        
        compra = Compra(fecha=fecha_compra, precio=medicamento.precio, idPaciente=paciente_compra)
        compra.save()
        
        compra_medicamento = CompraMedicamento(idMedicamento=medicamento, idCompra=compra)
        compra_medicamento.save()
        return redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and not user.is_staff), name='dispatch')# Paciente
class CompraMedicamentoDelete(LoginRequiredMixin, DeleteView):
    model = CompraMedicamento
    success_url = reverse_lazy('tienda')
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        medicamento_carrito = self.get_object()
        medicamento_carrito.delete()# del modelo CompraMedicamento
        
        paciente = Paciente.objects.get(username=self.request.user)
        medicamento = Compra.objects.get(idPaciente=paciente)
        medicamento.delete()
        
        messages.add_message(request, level=messages.WARNING, message="Medicamento eliminado de su carrito correctamente")
        return super().post(request, *args, **kwargs)


# Para limpiar las compras que ha realizado el paciente a la vez
@method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(lambda user: not user.is_superuser and not user.is_staff), name='dispatch')# Paciente
class CompraMedicamentoClearView(LoginRequiredMixin, ListView):
    model = CompraMedicamento
    template_name = "seguroprivado/tienda_medicamentos.html"
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(CompraMedicamentoClearView, self).get_context_data(**kwargs)
        
        compra_medicamento = CompraMedicamento.objects.all()
        compra_medicamento.delete()
        
        compras_paciente = Compra.objects.all()
        compras_paciente.delete()
        
        context['medicamentos'] = Medicamento.objects.all()
        return context