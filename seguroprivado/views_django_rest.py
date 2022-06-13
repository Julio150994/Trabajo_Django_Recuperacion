from datetime import datetime
from django.http import Http404
from django.contrib.auth.models import User
from seguroprivado.models import Cita, Paciente, Medico

# Importaciones para el API REST de Django
from seguroprivado.serializers import MedicoSerializers, CitaSerializers, UserSerializer
from lib2to3.pgen2.parse import ParseError
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

# Para permitir el acceso a los pacientes con un token generado #
class LoginAPIView(APIView):
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
            
        user = User.objects.get(username=data["user"])
        
        # Validamos las credenciales de usuario
        if "user" not in data or "password" not in data:
            return Response({
                'error': 'Credenciales de usuario erróneas'
            }, status = status.HTTP_401_UNAUTHORIZED)
        
        # Validación para el usuario del paciente
        if not user:
             return Response({
                 'error': 'Usuario no contemplado en el sistema'
             }, status = status.HTTP_404_NOT_FOUND)
        else:
            # Validamos que solamente puedan acceder usuarios que sean pacientes
            if user.is_superuser:
                return Response({
                    'error': 'Error. El usuario no debe ser administrador'
                }, status = status.HTTP_401_UNAUTHORIZED)
            else:
                if not user.is_superuser and user.is_staff:
                    return Response({
                        'error': 'Error. El usuario no debe ser médico'
                    }, status = status.HTTP_401_UNAUTHORIZED)
                else:
                    if not user.is_staff:
                        token, get_token = Token.objects.get_or_create(user=user)
                        
                        if get_token:
                            # Para generar un nuevo token, después de eliminarse el último utilizado
                            return Response({
                                'detail': 'El paciente '+str(user)+' ha iniciado sesión correctamente',
                                'token': token.key
                            }, status = status.HTTP_201_CREATED)
                        else:
                            token.delete()
                            return Response({
                                'error': 'Ya se ha iniciado sesión con este paciente',
                            }, status = status.HTTP_409_CONFLICT)
                    

# Para cerrar sesión de los pacientes eliminando el token de la sesión actual
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    token = list()
    
    def post(self, request, format=None):
        get_token = Token.objects.get(user=request.user)
        self.token.append(get_token)
        
        if get_token:
            request.user.auth_token.delete()
            
            # Cerramos la sesión eliminando el token
            return Response({
                'detail': 'El paciente '+str(request.user)+' ha cerrado sesión éxitosamente',
                'token': self.token[0].key
            }, status = status.HTTP_200_OK)


# Buscamos los usuarios de la base de datos
class UsuarioAPIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        usuario = User.objects.all()
        serializer_usuario = UserSerializer(usuario, many=True)
        return Response(serializer_usuario.data)

# Para poder seleccionar los médicos en la aplicación de ionic
class MedicosAPIView(APIView):
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


# Para encontrar el id del médico
class MedicoSeleccionadoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MedicoSerializers
    
    def get_queryset(self):
        medicos = Medico.objects.all()
        return medicos
    
    def get(self, request, format=None):
        try:
            medico_id = request.query_params["id"]
            
            if medico_id != None:
                medico = Medico.objects.get(id=medico_id)
                serializer_medico = MedicoSerializers(medico)
        except:
            medico = self.get_queryset()
            return Response({
                'error': 'Error. Médico no encontrado en el sistema',
            }, status = status.HTTP_404_NOT_FOUND)
        
        return Response(serializer_medico.data)

    
# Para obtener las citas del paciente con el médico seleccionado (herencia de clases)
class CitasPacienteApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    # Para obtener el médico seleccionado
    def get_object(self, pk):
        try:
            return Medico.objects.get(pk=pk)
        except Medico.DoesNotExist:
            raise Http404
        
    # Para obtener las citas realizadas del paciente que ha tenido con el médico seleccionado
    def get(self, request, pk, format=None):
        medico = self.get_object(pk)# encontramos el médico seleccionado
        print("Médico seleccionado: "+str(medico))
        paciente = Paciente.objects.get(username=request.user)
        
        fecha_cita_actual = datetime(int(datetime.today().year),int(datetime.today().month),int(datetime.today().day))
        formato_fecha_cita = datetime.strftime(fecha_cita_actual,'%Y-%m-%d')
        
        # Para citas realizadas menores que la fecha actual
        citas_paciente = Cita.objects.filter(idPaciente=paciente).filter(fecha__lte=formato_fecha_cita).filter(realizada=True)
        serializer_citas = CitaSerializers(citas_paciente, many=True)
        
        if citas_paciente.exists():
            return Response(serializer_citas.data, status=status.HTTP_200_OK)
        else:
             return Response({
                'detail': 'El paciente '+str(request.user)+' no tiene citas realizadas',
            }, status = status.HTTP_404_NOT_FOUND)