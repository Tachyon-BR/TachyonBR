from django import forms
from .models import TachyonUsuario

class CrearUsuarioForma(forms.Form):
    nombre = forms.CharField(max_length = 30)
    apellido_paterno = forms.CharField(max_length = 30)
    apellido_materno = forms.CharField(max_length = 30)
    telefono = forms.CharField(max_length = 15)
    estado = forms.CharField(max_length = 500)
    nombre_agencia = forms.CharField(max_length = 500, required=False)
    numero_agencia = forms.CharField(max_length = 500, required=False)
    contrasena = forms.CharField(max_length = 32, min_length=6)
    confirmar_contrasena = forms.CharField(max_length = 32, min_length=6)
    email = forms.EmailField()
