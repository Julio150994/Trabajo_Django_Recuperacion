from django.contrib import admin
from seguroprivado.models import Paciente

class PacienteAdmin(admin.ModelAdmin):
    list_display = ("nombre","apellidos","edad","direccion","foto","activo","username","password")
    search_fields = ("nombre","username",)
    list_filter = ("username",)
    ordering = ("-id",)


# Register your models here.

admin.site.register(Paciente)