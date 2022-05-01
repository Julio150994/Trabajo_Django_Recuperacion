from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from seguroprivado.models import Paciente

# Create your forms here.

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        
        help_texts = {
            'nombre': 'Debe escribir un nombre y que tenga un máximo de 30 caracteres.',
            'apellidos': 'Debe escribir unos apellidos y que formen un máximo de 50 caracteres.',
            'edad': 'Debe escribir una edad.',
            'direccion': 'Debe escribir una dirección.',
            'foto': 'Debe seleccionar una foto.',
            'username': 'Debe escribir un nombre de usuario y que tenga un máximo de 30 caracteres.',
            'password': 'Debe escribir una contraseña y que tenga un mínimo de 8 caracteres y un máximo de 30 caracteres.'
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control form-control-sm row', 'placeholder':'Escriba un nombre'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control form-control-sm row', 'placeholder':'Escriba unos apellidos'}),
            'edad': forms.NumberInput(attrs={'class':'form-control form-control-sm row', 'placeholder':'Escriba una edad'}),
            'direccion': forms.TextInput(attrs={'class':'form-control form-control-sm row', 'placeholder':'Escriba una dirección'}),
            'foto': forms.FileInput(attrs={'class':'form-control form-control-sm row'}),
            'username': forms.TextInput(attrs={'class':'form-control form-control-sm row', 'placeholder':'Escriba un nombre de usuario'}),
            'password':  forms.PasswordInput(attrs={'class':'form-control form-control-sm row', 'placeholder':'Escriba una contraseña'})   
        }
        
        error_messages = {
            'nombre': {'required': 'Debe escribir el nombre','max_length':'El nombre debe tener como máximo 30 caracteres'},
            'apellidos': {'required': 'Debe escribir unos apellidos', 'max_length':'Sus apellidos deben formar como máximo 50 caracteres'},
            'edad': {'required': 'Debe escribir una edad'},
            'direccion': {'required': 'Debe escribir una dirección'},
            'foto': {'required':'Debe seleccionar una foto'},
            'username': {'required': 'Debe escribir el nombre de usuario', 'max_length':'El nombre de usuario debe tener como máximo 30 caracteres'},
            'password': {'required': 'Debe escribir una contraseña', 'min_length': 'La contraseña debe tener como mínimo 8 caracteres', 'max_length':'La contraseña debe tener como máximo 30 caracteres'}
        }
    
        
    # Comprobamos que los datos del formulario sean correctos
    def clean_nombre(self):
        return self.cleaned_data['nombre']
    
    def clean_apellidos(self):
        return self.cleaned_data['apellidos']
    
    def clean_edad(self):
        return self.cleaned_data['edad']
    
    def clean_direccion(self):
        return self.cleaned_data['direccion']
    
    def clean_foto(self):
        return self.cleaned_data['foto']
    
    def clean_username(self):
        paciente = self.cleaned_data['username']
        
        if Paciente.objects.filter(username=paciente).exists():
            raise forms.ValidationError("El paciente "+str(paciente)+" ya está registrado, pruebe registrar otro.")
        return paciente
    
    def clean_password(self):
        return self.cleaned_data['password']