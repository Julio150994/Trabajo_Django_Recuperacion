from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from seguroprivado.models import Paciente, Medico, Cita

# Para llamar a nuestros usuarios
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user']

# Para hacer las funcionalidades de la api mediante serializers
class PacienteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['nombre','apellidos','edad','direccion','foto','activo','username']
        

class MedicoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id','nombre','apellidos','edad','fechaalta','especialidad','username']

class CitaSerializers(serializers.ModelSerializer):
    # Para relacionar entre serializers
    medico_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Cita
        fields = ['idMedico','medico_id','fecha','tratamiento','observaciones']
        depth = 1 # para bajar un nivel
    
    def to_representation(self, instance):
        return {
            'nombre': instance.idMedico.nombre,
            'apellidos': instance.idMedico.apellidos,
            'edad': instance.idMedico.edad,
            'fecha_alta': instance.idMedico.fechaalta,
            'especialidad': instance.idMedico.especialidad,
            'username': instance.idMedico.username,
            'fecha_cita': instance.fecha,
            'tratamiento': instance.tratamiento,
            'observaciones': instance.observaciones
        }