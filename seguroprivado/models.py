from django.db import models

# Create your models here.

class Medicos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, required=True, verbose_name="Nombre") 
    apellidos = models.CharField(max_length=50, required=True, verbose_name="Apellidos")
    edad = models.IntegerField(required=True, verbose_name="Edad")
    fechaalta = models.DateField(required=True, verbose_name="Fecha de alta")
    especialidad = models.CharField(max_length=40, required=True, verbose_name="Especialidad")
    username = models.CharField(max_length=30, required=True, verbose_name="Nombre de usuario")
    password = models.CharField(max_length=30, required=True, verbose_name="Contraseña")

    class Meta:
        verbose_name="médico"
        verbose_name_plural = "médicos"
        ordering = ["-id"]
    
    def __str__(self):
        return self.nombre+" "+self.apellidos+" "+str(self.edad)+" "+str(self.fechaalta)+" "+self.especialidad+" "+self.username+" "+self.password

class Medicamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, required=True, verbose_name="Nombre")
    descripcion = models.CharField(max_length=100, required=True, verbose_name="Descripción")
    receta = models.CharField(max_length=1, required=True,verbose_name="Receta")
    precio = models.FloatField(required=True, verbose_name="Precio")
    stock = models.IntegerField(verbose_name="Stock")
    
    class Meta:
        verbose_name="medicamento"
        verbose_name_plural = "médicamentos"
        ordering = ["-id"]

    def __str__(self):
        return self.nombre+" "+self.descripcion+" "+self.receta+" "+self.precio+" "+self.stock

class Pacientes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, required=True, verbose_name="Nombre") 
    apellidos = models.CharField(max_length=50, required=True, verbose_name="Apellidos")
    edad = models.IntegerField(required=True, verbose_name="Edad")
    direccion = models.CharField(max_length=100, required=True, verbose_name="Dirección")
    foto = models.ImageField(verbose_name="Foto", upload_to="pacientes",null=False, blank=False)
    username = models.CharField(max_length=30, required=True, verbose_name="Nombre de usuario")
    password = models.CharField(max_length=30, required=True, verbose_name="Contraseña")
    
    class Meta:
        verbose_name="paciente"
        verbose_name_plural = "pacientes"
        ordering = ["-id"]

    def __str__(self):
        return self.nombre+" "+self.apellidos+" "+str(self.edad)+" "+self.direccion+" "+str(self.foto)+" "+self.username+" "+self.password

class Citas(models.Model):
    id = models.AutoField(primary_key=True)
    idPaciente = models.ForeignKey(Pacientes, verbose_name="Paciente", on_delete=models.CASCADE)
    idMedico = models.ForeignKey(Medicos, verbose_name="Médico", on_delete=models.CASCADE)
    fecha = models.DateField(required=True, verbose_name="Fecha")
    observaciones = models.TextField(required=True, verbose_name="Observaciones")
    
    class Meta:
        verbose_name="cita"
        verbose_name_plural = "citas"
        ordering = ["-id"]

    def __str__(self):
        return str(self.idPaciente)+" "+str(self.idMedico)+" "+str(self.fecha)+" "+self.observaciones


class Compras(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(required=True, verbose_name="Fecha")
    precio = models.FloatField(required=True, verbose_name="Precio")
    idPaciente = models.ForeignKey(Pacientes, verbose_name="Paciente", on_delete=models.CASCADE)

    class Meta:
        verbose_name="compra"
        verbose_name_plural = "compras"
        ordering = ["-id"]
    
    def __str__(self):
        return str(self.fecha)+" "+str(self.precio)+" "+str(self.idPaciente)


class ComprasMedicamentos(models.Model):
    idMedicamento = models.ForeignKey(Medicamentos, verbose_name="Medicamento", on_delete=models.CASCADE)
    idCompra = models.ForeignKey(Compras, verbose_name="Compra", on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.idMedicamento)+" "+str(self.idCompra)