from django import forms
from seguroprivado.models import Paciente, Medico

# Create your forms here.

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
        exclude = ['activo']
        
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
            'nombre': forms.TextInput(attrs={'class':'form-control form-control-sm row mx-auto','placeholder':'Escriba un nombre', 'required':'required'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba unos apellidos', 'required':'required'}),
            'edad': forms.NumberInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba una edad', 'required':'required'}),
            'direccion': forms.TextInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba una dirección', 'required':'required'}),
            'foto': forms.FileInput(attrs={'class':'form-control form-control-sm row mx-auto', 'required':'required'}),
            'username': forms.TextInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba un nombre de usuario', 'required':'required'}),
            'password':  forms.PasswordInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba una contraseña', 'required':'required'})   
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
    
    # Comprobamos los datos introducidos, y si un paciente está o no registrado
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
        return self.cleaned_data['username']
    
    def clean_password(self):
        return self.cleaned_data['password']
    

class MedicoForm(forms.ModelForm):    
    class Meta:        
        model = Medico
        fields = '__all__'
        
        help_texts = {
            'nombre': 'Debe escribir un nombre y que tenga un máximo de 30 caracteres.',
            'apellidos': 'Debe escribir unos apellidos y que formen un máximo de 50 caracteres.',
            'edad': 'Debe introducir una edad.',
            'fechaalta': 'Debe introducir una fecha de alta.',
            'especialidad': 'Debe seleccionar una especialidad.',
            'username': 'Debe escribir un nombre de usuario y que tenga un máximo de 30 caracteres.',
            'password': 'Debe escribir una contraseña y que tenga un mínimo de 8 caracteres y un máximo de 30 caracteres.'
        }
        
        FA = 'familia'
        DI = 'digestivo'
        NE = 'neurólogo'
        DE = 'dermatólogo'
        TR = 'traumatólogo'
        
        especialidades = (
            (FA,'familia'),
            (DI,'digestivo'),
            (NE,'neurólogo'),
            (DE,'dermatólogo'),
            (TR,'traumatólogo')
        )
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba un nombre', 'required':'required'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba unos apellidos', 'required':'required'}),
            'edad': forms.NumberInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba una edad', 'required':'required'}),
            'fechaalta': forms.DateInput(format = ('%d/%m/%Y'), attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Fecha de alta', 'type':'date', 'required':'required'}),
            'especialidad': forms.Select(choices=especialidades ,attrs={'class':'form-control form-control-sm row mx-auto', 'required':'required'}),
            'username': forms.TextInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba nombre de usuario', 'required':'required'}),
            'password': forms.PasswordInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba una contraseña', 'required':'required'}) 
        }
        
        error_messages = {
            'nombre': {'required': 'Debe escribir el nombre','max_length':'El nombre debe tener como máximo 30 caracteres',},
            'apellidos': {'required': 'Debe escribir unos apellidos', 'max_length':'Sus apellidos deben formar como máximo 50 caracteres'},
            'edad': {'required': 'Debe introducir una edad'},
            'fechaalta': {'required': 'Debe escribir una fecha de alta'},
            'especialidad': {'required':'Debe seleccionar una especialidad'},
            'username': {'required': 'Debe escribir el nombre de usuario', 'max_length':'El nombre de usuario debe tener como máximo 30 caracteres'},
            'password': {'required': 'Debe escribir una contraseña', 'min_length': 'La contraseña debe tener como mínimo 8 caracteres', 'max_length':'La contraseña debe tener como máximo 30 caracteres'}
        }
    
    # Comprobamos los datos del médico que se hayan introducido #
    def clean_nombre(self):
        return self.cleaned_data['nombre']
    
    def clean_apellidos(self):
        return self.cleaned_data['apellidos']
    
    def clean_edad(self):
        return self.cleaned_data['edad']
    
    def clean_fechaalta(self):
        return self.cleaned_data['fechaalta']
    
    def clean_especialidad(self):
        return self.cleaned_data['especialidad']
    
    def clean_username(self):
        return self.cleaned_data['username']
    
    def clean_password(self):
        return self.cleaned_data['password']
    

class MedicamentoForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        
        labels = {
            'nombre': ('Nombre'),
            'descripcion': ('Descripción'),
            'receta': ('Receta'),
            'precio': ('Precio'),
            'stock': ('Número de stock')
        }
        
        help_texts = {
            'nombre': 'Debe escribir un nombre y que tenga un máximo de 50 caracteres.',
            'descripcion': 'Debe escribir unos apellidos y que formen un máximo de 50 caracteres.',
            'receta':'Debe seleccionar si tiene o no receta.',
            'precio':'Debe introducir un precio y que tenga dos decimales.',
            'stock':'El stock no debe ser cero.'
        }
        
        CON = 's'
        SIN = 'n'
    
        recetas = (
            (CON,'Con receta'),
            (SIN,'Sin receta'),
        )
        
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba un nombre de receta'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control form-control-sm row mx-auto', 'placeholder':'Escriba una descripción'}),
            'receta': forms.Select(choices=recetas ,attrs={'class':'form-control form-control-sm row mx-auto'}),
            'precio': forms.NumberInput(attrs={'class':'form-control form-control-sm row mx-auto', 'type':'float'}),
            'stock': forms.NumberInput(attrs={'class':'form-control form-control-sm row mx-auto', 'type':'int'})
        }
        
        error_messages = {
            'nombre': {'required': 'Debe escribir el nombre','max_length':'El nombre debe tener como máximo 50 caracteres.',},
            'descripcion': {'required': 'Debe escribir unos apellidos', 'max_length':'La descripción no puede tener más de 100 caracteres.'},
            'receta': {'required':'Debe seleccionar si tiene o no receta.'},
            'precio': {'required': 'Debe escribir un precio'},
            'stock': {'required': 'Debe poner un número de stock'}
        }
    
    # Añadimos o editamos medicamentos #
    def save(self, commit=True):
        medicamento = super(MedicamentoForm, self).save()
        medicamento.nombre = self.cleaned_data["nombre"]
        medicamento.descripcion = self.cleaned_data["descripcion"]
        medicamento.receta = self.cleaned_data["receta"]
        medicamento.precio = self.cleaned_data["precio"]
        medicamento.stock = self.cleaned_data["stock"]
        medicamento.save()
        return medicamento