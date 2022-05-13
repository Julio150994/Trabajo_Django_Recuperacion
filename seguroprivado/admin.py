from django.contrib import admin
from seguroprivado.models import Paciente, Medico, Medicamento

class MedicoAdmin(admin.ModelAdmin):
    list_display = ["nombre","apellidos","edad","fechaalta","especialidad","username","password"]
    ordering = ["-id"]
    
class PacienteAdmin(admin.ModelAdmin):
    list_display = ["nombre","apellidos","edad","direccion","foto","activo","username","password"]
    ordering = ["-id"]
    
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ["nombre","descripcion","receta","precio","stock"]
    ordering = ["-id"]

# Register your models here.

admin.site.register(Medico, MedicoAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medicamento, MedicamentoAdmin)