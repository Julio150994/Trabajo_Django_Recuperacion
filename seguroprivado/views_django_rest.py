from datetime import datetime
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from seguroprivado.models import Cita, Paciente, Medico
from django.db.models import Q

# Importaciones para el API REST de Django
from seguroprivado.serializers import MedicoSerializers, CitaSerializers
from lib2to3.pgen2.parse import ParseError
from collections import OrderedDict
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication, permissions

# Para permitir el acceso a los pacientes con un token generado #
class TokenRestView(APIView):
    def get(self, request, format=None):
        return Response({'detail':"Respuesta para el paciente"})
    
    def post(self, request, format=None, *args, **kwargs):
        try:
            data = request.data
        except ParseError as error:
            return Response(
                'Formato JSON inválido - {0}'.format(error.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if "user" not in data or "password" not in data:
            return Response(
                'Error al introducir las credenciales de usuario',
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user = User.objects.get(username=data["user"])
        
        # Validación para el usuario del paciente
        if not user:
             return Response(
                'Paciente no encontrado en el sistema.',
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            # Validamos que es un usuario paciente
            if not user.is_staff:
                token, get_token = Token.objects.get_or_create(user=user)
                
                if get_token:
                    # Para generar un nuevo token, después de eliminarse el último utilizado
                    return Response({
                        'detail': 'El paciente ha iniciado sesión correctamente',
                        'token': token.key
                    }, status = status.HTTP_201_CREATED)
                else:
                    token.delete()
                    Response({
                        'error': 'Ya se ha iniciado sesión con este paciente',
                    }, status = status.HTTP_409_CONFLICT)
            else:
                return Response({
                    'detail': 'Error. El usuario debe ser un paciente'
                }, status= status.HTTP_401_UNAUTHORIZED)

# Para cerrar sesión de los pacientes
class LogoutAPIView(APIView):
   def get(self, request, *args, **kwargs):
       token = request.GET.get('token')
       token_paciente = Token.objects.filter(key=token).first()
       
       if token_paciente:
            paciente = token_paciente.user

# Para poder seleccionar los médicos en la aplicación de ionic
class MedicoApiView(APIView):
    # Para acceder solamente si hemos iniciado sesión
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None, *args, **kwargs):
        medico = Medico.objects.all()
        serializer_medico = MedicoSerializers(medico, many=True)
        return Response(serializer_medico.data)
    
    def post(self, request, format=None):
        serializer_medico = MedicoSerializers(data=request.data)
        if serializer_medico.is_valid():
            return Response(serializer_medico.data, status=status.HTTP_200_OK)
        return Response(serializer_medico.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CitasPacienteApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    # Para obtener el médico seleccionado
    def get_object(self, pk):
        try:
            return Medico.objects.get(pk=pk)
        except Medico.DoesNotExist:
            raise Http404
        
    # Para obtener las citas realizadas del paciente que ha tenido con el médico seleccionado
    def get(self, request, format=None):
        #medico = self.get_object(pk) # cuando seleccionemos médico
        paciente = Paciente.objects.get(username=request.user)
        
        fecha_cita_actual = datetime(int(datetime.today().year),int(datetime.today().month),int(datetime.today().day))
        formato_fecha_cita = datetime.strftime(fecha_cita_actual,'%Y-%m-%d')
        
        # Para citas realizadas menores que la fecha actual
        citas_paciente = Cita.objects.filter(idPaciente=paciente).filter(fecha__lte=formato_fecha_cita).filter(realizada=True)
        serializer_citas = CitaSerializers(citas_paciente, many=True)
        
        if citas_paciente.exists():
            return Response(serializer_citas.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer_citas.errors, status=status.HTTP_400_BAD_REQUEST)