from django.contrib import admin
from django import forms
from seguroprivado.forms import MedicamentoForm
from seguroprivado.models import Paciente, Medico, Medicamento, Cita, Compra, CompraMedicamento
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from datetime import datetime
import re

# Clases para establecer las validaciones en el panel de admin
class MedicoAdminForm(forms.ModelForm):
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        
        if len(nombre) > 30:
            raise forms.ValidationError('El nombre del médico debe tener 30 caracteres como máximo')
        else:
            return nombre
        
    def clean_apellidos(self):
        apellidos = self.cleaned_data['apellidos']
        
        if len(apellidos) > 50:
            raise forms.ValidationError('Los apellidos deben comprender 50 caracteres como máximo')
        else:
            return apellidos
        
    def clean_edad(self):
        edad = self.cleaned_data['edad']
        
        if edad < 0:
            raise forms.ValidationError('La edad '+str(edad)+" no es válida")
        else:
            return edad
        
    def clean_fechaalta(self):
        fechaalta = self.cleaned_data['fechaalta']
        
        set_fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
        set_fecha_alta = datetime.strptime(str(fechaalta),'%Y-%m-%d')
        
        if set_fecha_alta <= set_fecha_actual:
            raise forms.ValidationError('La fecha de alta no debe ser menor o igual que la fecha actual')
        else:
            return fechaalta
    
    def clean_username(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        if Medico.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario médico '+str(username)+' ya existe')
        else:
            if len(username) > 30:
                raise forms.ValidationError('El nombre de usuario debe tener 30 caracteres como máximo')
            else:
                if User.objects.filter(username=username).exists() or not User.objects.filter(username=username).exists():
                    # Para editar un usuario médico
                    get_medico = User.objects.get(username=username)
                    get_medico.delete()
                    
                    usuario_medico = User.objects.create(username=username, password=make_password(password))
                    usuario_medico.is_staff = True
                    usuario_medico.save()
                else:
                    # Para añadir un usuario médico
                    medico = User.objects.create(username=username, password=make_password(password))
                    medico.is_staff = True
                    medico.save()
                    
                return username
        
    def clean_password(self):
        password = self.cleaned_data['password']
        
        if len(password) > 30:
            raise forms.ValidationError('La contraseña del médico debe tener 30 caracteres como máximo')
        else:   
            re_medico = re.findall(r'^(0|[1-9]\d*)$', password)
            
            if not re_medico:
                raise forms.ValidationError('La contraseña del paciente no puede ser completamente numérica')
            else:
                return password

class MedicamentoAdminForm(forms.ModelForm):
    form = MedicamentoForm
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        
        if Medicamento.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError('El nombre de medicamento '+str(nombre)+' ya existe.')
        else:
            if len(nombre) > 50:
                raise forms.ValidationError('El nombre '+str(nombre)+' debe tener 50 caracteres como máximo')
            else:
                return nombre
        
    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']

        if len(descripcion) > 100:
            raise forms.ValidationError('La descripción debe tener 100 caracteres como máximo')
        else:
            return descripcion
    
    def clean_precio(self):
        precio = self.cleaned_data['precio']
        
        get_decimales = str(precio)[str(precio).find(".")+1:]
    
        if len(get_decimales) != 2:
            raise forms.ValidationError('El número de precio debe contener dos decimales')
        else:
            return precio
        
    def clean_stock(self):
        stock = self.cleaned_data['stock']
        
        if not stock:
            raise forms.ValidationError('Debe poner un número de stock')
        else:
            return stock

class PacienteAdminForm(forms.ModelForm):
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
                    
        if len(nombre) > 30:
            raise forms.ValidationError('El nombre del paciente debe tener 30 caracteres como máximo')
        else:
            return nombre
        
    def clean_apellidos(self):
        apellidos = self.cleaned_data['apellidos']
        
        if len(apellidos) > 50:
            raise forms.ValidationError('Los apellidos deben comprender 50 caracteres como máximo')
        else:
            return apellidos
        
    def clean_edad(self):
        edad = self.cleaned_data['edad']
        
        if edad < 0:
            raise forms.ValidationError('La edad para el paciente no es válida')
        else:
            return edad
        
    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        
        if len(direccion) > 100:
            raise forms.ValidationError('La dirección debe tener 100 caracteres como máximo')
        else:
            return direccion
        
    def clean_foto(self):
        foto = self.cleaned_data['foto']
        
        if foto is None:
            raise forms.ValidationError('Debe seleccionar una foto para el paciente')
        else:
            return foto
    
    def clean_username(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        if Paciente.objects.filter(username=username).exists():              
            if len(username) > 30:
                raise forms.ValidationError('El nombre de usuario debe tener 30 caracteres como máximo')
            else:
                if User.objects.filter(username=username).exists() or not User.objects.filter(username=username).exists():
                    # Para editar un usuario paciente
                    get_medico = User.objects.get(username=username)
                    get_medico.delete()
                    
                    usuario_medico = User.objects.create(username=username, password=make_password(password))
                    usuario_medico.save()
                else:
                    # Para añadir un usuario paciente
                    User.objects.create(username=username, password=make_password(password))
                return username
        
    def clean_password(self):        
        password = self.cleaned_data['password']
        
        if len(password) < 8 and len(password) > 30:
            raise forms.ValidationError('La contraseña del paciente debe tener entre 8 y 30 caracteres')
        else:
            re_paciente = re.findall(r'^(0|[1-9]\d*)$', password)
            
            if not re_paciente:
                raise forms.ValidationError('La contraseña del paciente no puede ser completamente numérica')
            else:
                return password

class CitaAdminForm(forms.ModelForm):
    def clean_idPaciente(self):
        id_paciente = self.cleaned_data['idPaciente']
        
        if id_paciente is None:
            raise forms.ValidationError('Debe seleccionar un paciente')
        else:
            return id_paciente
        
    def clean_idMedico(self):
        id_medico = self.cleaned_data['idMedico']
        
        if id_medico is None:
            raise forms.ValidationError('Debe seleccionar un médico')
        else:
            return id_medico
    
    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        
        set_fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
        set_fecha_cita = datetime.strptime(str(fecha),'%Y-%m-%d')
        
        if set_fecha_cita < set_fecha_actual:
            raise forms.ValidationError('La fecha de la cita debe ser mayor o igual que la fecha actual')
        else:
            return fecha
    
    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        
        if len(observaciones) > 100:
            raise forms.ValidationError('Las observaciones debe contener 100 caracteres como máximo')
        else:
            return observaciones

class CompraAdminForm(forms.ModelForm):
    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']

        set_fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
        set_fecha_compra = datetime.strptime(str(fecha),'%Y-%m-%d')
        
        if set_fecha_compra > set_fecha_actual:
            raise forms.ValidationError('La fecha de compra no debe ser mayor que la fecha actual')
        else:
            return fecha
            
    def clean_precio(self):
        precio = self.cleaned_data['precio']
        
        get_decimales = str(precio)[str(precio).find(".")+1:]
    
        if len(get_decimales) != 2:
            return forms.ValidationError('El precio de la compra debe contener dos decimales')
        else:
            return precio
    
    def clean_idPaciente(self):
        id_paciente = self.cleaned_data['idPaciente']
        
        if id_paciente is None:
            raise forms.ValidationError('Debe seleccionar un paciente para la compra de medicamento')
        else:
            return id_paciente
    
class CompraMedicamentoAdminForm(forms.ModelForm):
    def clean_idMedicamento(self):
        id_medicamento = self.cleaned_data['idMedicamento']
        
        if id_medicamento is None:
            raise forms.ValidationError('Debe seleccionar un medicamento comprado por el paciente')
        else:
            return id_medicamento
    
    def clean_idPaciente(self):
        id_paciente = self.cleaned_data['idPaciente']
        
        if id_paciente is None:
            raise forms.ValidationError('Debe seleccionar un paciente para la compra de medicamento')
        else:
            return id_paciente

# Para establecer relaciones entre los modelos
class MedicoInline(admin.StackedInline):
    model = Medico
    
class MedicamentoInline(admin.StackedInline):
    model = Medicamento
    
class PacienteInline(admin.StackedInline):
    model = Paciente
    
class CitaInline(admin.StackedInline):
    model = Cita
    
class CompraInline(admin.StackedInline):
    model = Compra
    
class CompraMedicamentoInline(admin.StackedInline):
    model = CompraMedicamento


class MedicoAdmin(admin.ModelAdmin):
    form = MedicoAdminForm
    
    # Cambiamos el formato de fecha de alta del médico
    def fecha_alta(self, obj):
        return obj.fechaalta.strftime("%d/%m/%Y")
    
    list_display = ["nombre","apellidos","edad","fecha_alta","especialidad","username","password"]
    search_fields = ["nombre","username",]
    list_filter = ["username",]
    ordering = ["-id",]
    list_per_page = 3
    
class PacienteAdmin(admin.ModelAdmin):
    form = PacienteAdminForm
    list_display = ["nombre","apellidos","edad","direccion","foto","activo","username","password"]
    search_fields = ["nombre","username",]
    list_filter = ["username",]
    ordering = ["-id",]
    list_per_page = 3

class MedicamentoAdmin(admin.ModelAdmin):    
    form = MedicamentoForm
    list_display = ["nombre","descripcion","precio","receta","stock"]
    search_fields = ["nombre",]
    list_filter = ["nombre","descripcion","precio","receta",]
    ordering = ["-id",]
    list_per_page = 3

class CitaAdmin(admin.ModelAdmin):
    form = CitaAdminForm
    
    # Cambiamos el formato de fecha de alta del médico
    def fecha_cita(self, obj):
        return obj.fecha.strftime("%d/%m/%Y")
    
    list_display = ["idPaciente","idMedico","fecha_cita","observaciones"]
    search_fields = ["idPaciente","idMedico",]
    list_filter = ["idPaciente","idMedico",]
    ordering = ["-id",]
    list_per_page = 3
    
class CompraAdmin(admin.ModelAdmin):
    form = CompraAdminForm
    
    # Cambiamos el formato de fecha de alta del médico
    def fecha_compra(self, obj):
        return obj.fecha.strftime("%d/%m/%Y")
    
    list_display = ["fecha_compra","precio","idPaciente"]
    search_fields = ["idPaciente",]
    list_filter = ["idPaciente",]
    ordering = ["-id",]
    list_per_page = 3
    
class CompraMedicamentoAdmin(admin.ModelAdmin):
    form = CompraMedicamentoAdminForm
    list_display = ["idMedicamento","idCompra"]
    search_fields = ["idMedicamento","idCompra",]
    list_filter = ["idMedicamento",]
    ordering = ["-id",]
    list_per_page = 3

# Register your models here.

admin.site.register(Medico, MedicoAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medicamento, MedicamentoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(CompraMedicamento, CompraMedicamentoAdmin)