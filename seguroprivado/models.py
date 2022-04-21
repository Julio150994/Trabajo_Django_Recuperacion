from django.db import models

# Create your models here.

class Medicos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False, blank=False, verbose_name="Nombre") 
    apellidos = models.CharField(max_length=50, null=False, blank=False, verbose_name="Apellidos")
    edad = models.IntegerField(null=False, blank=False, verbose_name="Edad")
    fechaalta = models.DateField(null=False, blank=False, verbose_name="Fecha de alta")
    especialidad = models.CharField(max_length=40, null=False, blank=False, verbose_name="Especialidad")
    username = models.CharField(max_length=30, unique=True, null=False, blank=False, verbose_name="Nombre de usuario")
    password = models.CharField(max_length=30, null=False, blank=False, verbose_name="Contraseña")

    class Meta:
        verbose_name="médico"
        verbose_name_plural = "médicos"
        ordering = ["-id"]
    
    def __str__(self):
        return self.nombre+" "+self.apellidos+" "+str(self.edad)+" "+str(self.fechaalta)+" "+self.especialidad+" "+self.username+" "+self.password

class Medicamentos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False, blank=False, verbose_name="Nombre")
    descripcion = models.CharField(max_length=100, null=False, blank=False, verbose_name="Descripción")
    receta = models.CharField(max_length=1, null=False, blank=False, verbose_name="Receta")
    precio = models.FloatField(null=False, blank=False, verbose_name="Precio")
    stock = models.IntegerField(null=False, blank=False, verbose_name="Stock")
    
    class Meta:
        verbose_name="medicamento"
        verbose_name_plural = "médicamentos"
        ordering = ["-id"]

    def __str__(self):
        return self.nombre+" "+self.descripcion+" "+self.receta+" "+str(self.precio)+" "+str(self.stock)

class Pacientes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, null=False, blank=False, verbose_name="Nombre") 
    apellidos = models.CharField(max_length=50, null=False, blank=False, verbose_name="Apellidos")
    edad = models.IntegerField(null=False, blank=False, verbose_name="Edad")
    direccion = models.CharField(max_length=100, null=False, blank=False, verbose_name="Dirección")
    foto = models.ImageField(upload_to="pacientes/", verbose_name="Foto", null=False, blank=False)
    username = models.CharField(max_length=30, unique=True, null=False, blank=False, verbose_name="Nombre de usuario")
    password = models.CharField(max_length=30, null=False, blank=False, verbose_name="Contraseña")
    
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
    fecha = models.DateField(null=False, blank=False, verbose_name="Fecha")
    observaciones = models.TextField(null=False, blank=False, verbose_name="Observaciones")
    
    class Meta:
        verbose_name="cita"
        verbose_name_plural = "citas"
        ordering = ["-id"]

    def __str__(self):
        return str(self.idPaciente)+" "+str(self.idMedico)+" "+str(self.fecha)+" "+self.observaciones


class Compras(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField(null=False, blank=False, verbose_name="Fecha")
    precio = models.FloatField(null=False, blank=False, verbose_name="Precio")
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