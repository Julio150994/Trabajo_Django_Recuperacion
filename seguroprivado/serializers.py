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
        fields = ['user','password']

# Para hacer las funcionalidades de la api mediante serializers
class PacienteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = ['nombre','apellidos','edad','direccion','foto','activo','username']
        

class MedicoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['nombre','apellidos','edad','fechaalta','especialidad','username']

class CitaSerializers(serializers.ModelSerializer):
    paciente_id = serializers.IntegerField(write_only=True)
    medico_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Cita
        fields = ['idPaciente','paciente_id','idMedico','medico_id','fecha','tratamiento','observaciones']
        depth = 1 # para bajar un nivel