from django.contrib import admin
from django import forms
from seguroprivado.models import Paciente, Medico, Medicamento, Cita, Compra, CompraMedicamento

# Clases para establecer las validaciones en el panel de admin
class MedicoAdminForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if username is None:
            return forms.ValidationError('Debe introducir un nombre de usuario para el médico')
        else:
            if len(username) < 30:
                return forms.ValidationError(str(username)+' debe tener 30 ó más caracteres')
            return username

class MedicamentoAdminForm(forms.ModelForm):
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']

        if nombre is None:
            return forms.ValidationError('Debe introducir un nombre para el medicamento')
        else:
            if len(nombre) < 50:
                return forms.ValidationError('El nombre '+str(nombre)+' debe tener 50 ó más caracteres')
            return nombre

class PacienteAdminForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if username is None:
            return forms.ValidationError('Debe introducir un nombre de usuario para el paciente')
        else:
            if len(username) < 30:
                return forms.ValidationError(str(username)+' debe tener 30 ó más caracteres')
            return username

class CitaAdminForm(forms.ModelForm):
    def clean_observaciones(self):
        observaciones = self.cleaned_data['observaciones']
        if observaciones is None:
            return forms.ValidationError('Debe introducir un nombre de usuario para el médico')
        else:
            return observaciones

class CompraAdminForm(forms.ModelForm):
    def clean_fecha(self):
        fecha_compra = self.cleaned_data['fecha']

        if fecha_compra is None:
            return forms.ValidationError('Debe escribir una fecha de compra')

class CompraMedicamentoAdminForm(forms.ModelForm):
    pass

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
    list_display = ["nombre","apellidos","edad","fechaalta","especialidad","username","password"]
    search_fields = ["nombre","username",]
    list_filter = ["username",]
    #list_editable = ["nombre","apellidos","edad","fechaalta","especialidad","username","password"]
    ordering = ["-id",]
    list_per_page = 3
    
class PacienteAdmin(admin.ModelAdmin):
    list_display = ["nombre","apellidos","edad","direccion","foto","activo","username","password"]
    search_fields = ["nombre","username",]
    list_filter = ["username",]
    #list_editable = ["nombre","apellidos","edad","direccion","foto","activo","username","password",]
    ordering = ["-id",]
    list_per_page = 3
    
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ["nombre","descripcion","precio","stock"]
    search_fields = ["nombre",]
    list_filter = ["nombre","descripcion","precio",]
    #list_editable = ["nombre","descripcion","precio",]
    ordering = ["-id",]
    list_per_page = 3

class CitaAdmin(admin.ModelAdmin):
    list_display = ["idPaciente","idMedico","fecha","observaciones"]
    search_fields = ["idPaciente","idMedico",]
    list_filter = ["idPaciente","idMedico",]
    #list_editable = ["fecha","observaciones"]
    ordering = ["-id",]
    list_per_page = 3
    #inlines = [PacienteInline, MedicoInline]

class CompraAdmin(admin.ModelAdmin):
    list_display = ["fecha","precio","idPaciente"]
    search_fields = ["idPaciente",]
    list_filter = ["idPaciente",]
    #list_editable = ["fecha","precio"]
    ordering = ["-id",]
    list_per_page = 3
    #inlines = [PacienteInline]

class CompraMedicamentoAdmin(admin.ModelAdmin):
    list_display = ["idMedicamento","idCompra"]
    search_fields = ["idMedicamento","idCompra",]
    list_filter = ["idMedicamento",]
    ordering = ["-id",]
    list_per_page = 3
    #inlines = [MedicamentoInline]

# Register your models here.

admin.site.register(Medico, MedicoAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medicamento, MedicamentoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(CompraMedicamento, CompraMedicamentoAdmin)