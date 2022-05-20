from django.contrib import admin
from django import forms
from seguroprivado.models import Paciente, Medico, Medicamento, Cita, Compra, CompraMedicamento
from datetime import datetime

# Clases para establecer las validaciones en el panel de admin
class MedicoAdminForm(forms.ModelForm):
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        
        if nombre is None:
            raise forms.ValidationError('Debe introducir un nombre para el médico')
        else:
            if len(nombre) > 30:
                raise forms.ValidationError('El nombre del médico debe tener 30 caracteres como máximo')
            else:
                return nombre
        
    def clean_apellidos(self):
        apellidos = self.cleaned_data['apellidos']
        
        if apellidos is None:
            raise forms.ValidationError('Debe introducir los apellidos para el médico')
        else:
            if len(apellidos) > 50:
                raise forms.ValidationError('Los apellidos deben comprender 50 caracteres como máximo')
            else:
                return apellidos
        
    def clean_edad(self):
        edad = self.cleaned_data['edad']
        
        if edad is None:
            raise forms.ValidationError('Debe introducir una edad para el médico')
        else:
            if edad < 0:
                raise forms.ValidationError('La edad '+str(edad)+" no es válida")
            else:
                return edad
        
    def clean_fechaalta(self):
        fechaalta = self.cleaned_data['fechaalta']
        
        if fechaalta is None:
            raise forms.ValidationError('Debe introducir una fecha de alta para el médico')
        else:
            set_fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
            set_fecha_alta = datetime.strptime(fechaalta,'%Y-%m-%d')
            
            if set_fecha_alta <= set_fecha_actual:
                raise forms.ValidationError('La fecha de alta no debe ser menor o igual que la fecha actual')
            else:
                return fechaalta
        
    def clean_especialidad(self):
        especialidad = self.cleaned_data['especialidad']
        
        if especialidad is None:
            raise forms.ValidationError('Debe seleccionar una especialidad')
        else:
            return especialidad
    
    def clean_username(self):
        username = self.cleaned_data['username']
        
        if username is None:
            raise forms.ValidationError('Debe introducir un nombre de usuario para el médico')
        else:
            if Medico.objects.filter(username=username).exists():
                raise forms.ValidationError('El nombre de usuario médico '+str(username)+' ya existe')
            else:
                if len(username) > 30:
                    raise forms.ValidationError('El nombre de usuario debe tener 30 caracteres como máximo')
                else:
                    return username
        
    def clean_password(self):
        password = self.cleaned_data['password']
        
        if password is None:
            raise forms.ValidationError('Debe introducir una contraseña para el médico')
        else:
            if len(password) > 30:
                raise forms.ValidationError('La contraseña del médico debe tener 30 caracteres como máximo')
            else:
                return password

class MedicamentoAdminForm(forms.ModelForm):
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        
        if nombre is None:
            raise forms.ValidationError('Debe introducir un nombre para el medicamento')
        else:
            if Medicamento.objects.filter(nombre=nombre).exists():
                raise forms.ValidationError('El nombre de medicamento '+str(nombre)+' ya existe.')
            else:
                if len(nombre) > 50:
                    raise forms.ValidationError('El nombre '+str(nombre)+' debe tener 50 caracteres como máximo')
                else:
                    return nombre
        
    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']

        if descripcion is None:
            raise forms.ValidationError('Debe introducir una descripción para el medicamento')
        else:
            if len(descripcion) > 100:
                raise forms.ValidationError('La descripción debe tener 100 caracteres como máximo')
            else:
                return descripcion
        
    def clean_receta(self):
        receta = self.cleaned_data['receta']
        
        if receta is None:
            raise forms.ValidationError('Debe seleccionar una receta')
        else:
            return receta
        
    def clean_precio(self):
        precio = self.cleaned_data['precio']
        
        if precio is None:
            raise forms.ValidationError('Debe introducir un precio')
        else:
            get_decimales = str(precio)[str(precio).find(".")+1:]
        
            if len(get_decimales) != 2:
                raise forms.ValidationError('El número de precio debe contener dos decimales')
            else:
                return precio


class PacienteAdminForm(forms.ModelForm):
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if nombre is None:
            raise forms.ValidationError('Debe introducir un nombre para el paciente')
        else:            
            if len(nombre) > 30:
                raise forms.ValidationError('El nombre del médico debe tener 30 caracteres como máximo')
            else:
                return nombre
        
    def clean_apellidos(self):
        apellidos = self.cleaned_data['apellidos']
        if apellidos is None:
            raise forms.ValidationError('Debe introducir los apellidos para el paciente')
        else:
            if len(apellidos) > 50:
                raise forms.ValidationError('Los apellidos deben comprender 50 caracteres como máximo')
            else:
                return apellidos
        
    def clean_edad(self):
        edad = self.cleaned_data['edad']
        if edad is None:
            raise forms.ValidationError('Debe introducir una edad para el paciente')
        else:
            if edad < 0:
                raise forms.ValidationError('La edad para el paciente no es válida')
            else:
                return edad
        
    def clean_direccion(self):
        direccion = self.cleaned_data['direccion']
        if direccion is None:
            raise forms.ValidationError('Debe escribir una dirección para el paciente')
        else:
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
        if username is None:
            raise forms.ValidationError('Debe introducir un nombre de usuario para el paciente')
        else:
            if Paciente.objects.filter(username=username).exists():    
                if len(username) > 30:
                    raise forms.ValidationError('El nombre de usuario debe tener 30 caracteres como máximo')
                else:
                    return username
        
    def clean_password(self):
        password = self.cleaned_data['password']
        if password is None:
            raise forms.ValidationError('Debe introducir una contraseña para el paciente')
        else:
            if len(password) > 30:
                raise forms.ValidationError('La contraseña del paciente debe tener 30 caracteres como máximo')
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
        
        if fecha is None:
            raise forms.ValidationError('Debe introducir una fecha de cita para el paciente')
        else:
            set_fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
            set_fecha_cita = datetime.strptime(fecha,'%Y-%m-%d')
            
            if set_fecha_cita <= set_fecha_actual:
                raise forms.ValidationError('La fecha de la cita no debe ser menor o igual que la fecha actual')
            else:
                return fecha
    
    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        if observaciones is None:
            raise forms.ValidationError('Debe introducir un nombre de usuario para el médico')
        else:
            if len(observaciones) > 100:
                raise forms.ValidationError('Las observaciones debe contener 100 caracteres como máximo')
            else:
                return observaciones

class CompraAdminForm(forms.ModelForm):
    def clean_fecha(self):
        fecha_compra = self.cleaned_data['fecha']

        if fecha_compra is None:
            raise forms.ValidationError('Debe introducir una fecha de compra del paciente')
        else:
            set_fecha_actual = datetime(int(datetime.now().year),int(datetime.now().month),int(datetime.now().day))
            set_fecha_compra = datetime.strptime(fecha_compra,'%Y-%m-%d')
            
            if set_fecha_compra > set_fecha_actual:
                raise forms.ValidationError('La fecha de compra no debe ser mayor que la fecha actual')
            else:
                return fecha_compra
            
    def clean_precio(self):
        precio = self.cleaned_data['precio']
        
        if precio is None:
            raise forms.ValidationError('Debe introducir un precio de compra')
        else:
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
    list_display = ["nombre","apellidos","edad","fechaalta","especialidad","username","password"]
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
    form = MedicamentoAdminForm
    list_display = ["nombre","descripcion","precio","stock"]
    search_fields = ["nombre",]
    list_filter = ["nombre","descripcion","precio",]
    ordering = ["-id",]
    list_per_page = 3

class CitaAdmin(admin.ModelAdmin):
    form = CitaAdminForm
    list_display = ["idPaciente","idMedico","fecha","observaciones"]
    search_fields = ["idPaciente","idMedico",]
    list_filter = ["idPaciente","idMedico",]
    ordering = ["-id",]
    list_per_page = 3

class CompraAdmin(admin.ModelAdmin):
    form = CompraAdminForm
    list_display = ["fecha","precio","idPaciente"]
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