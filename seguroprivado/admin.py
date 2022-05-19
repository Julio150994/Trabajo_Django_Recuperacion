from django.contrib import admin
from seguroprivado.models import Paciente, Medico, Medicamento, Cita, Compra, CompraMedicamento

class MedicoAdmin(admin.ModelAdmin):
    list_display = ["nombre","apellidos","edad","fechaalta","especialidad","username","password"]
    search_fields = ["nombre","username",]
    list_filter = ["username",]
    ordering = ["-id"]
    
class PacienteAdmin(admin.ModelAdmin):
    list_display = ["nombre","apellidos","edad","direccion","foto","activo","username","password"]
    search_fields = ["nombre","username",]
    list_filter = ["username",]
    ordering = ["-id"]
    
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ["nombre","descripcion","precio","stock"]
    search_fields = ["nombre",]
    list_filter = ["nombre",]
    ordering = ["-id"]

class CitaAdmin(admin.ModelAdmin):
    list_display = ["idPaciente","idMedico","fecha","observaciones"]
    search_fields = ["idPaciente","idMedico",]
    list_filter = ["idPaciente","idMedico",]
    ordering = ["-id"]

class CompraAdmin(admin.ModelAdmin):
    list_display = ["fecha","precio","idPaciente"]
    search_fields = ["idPaciente",]
    list_filter = ["idPaciente",]
    ordering = ["-id"]

class CompraMedicamentoAdmin(admin.ModelAdmin):
    list_display = ["idMedicamento","idCompra"]
    search_fields = ["idMedicamento","idCompra",]
    list_filter = ["idMedicamento",]
    ordering = ["-id"]

# Register your models here.

admin.site.register(Medico, MedicoAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medicamento, MedicamentoAdmin)
admin.site.register(Cita, CitaAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(CompraMedicamento, CompraMedicamentoAdmin)