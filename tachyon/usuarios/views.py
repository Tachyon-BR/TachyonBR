from django.shortcuts import render
from django.http import Http404
from .forms import CrearUsuarioForma
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
import time
import string
from .models import *

# Create your views here.

# Vista de registro de Usuarios
def create(request):
    return render(request, 'usuarios/create.html')


# Vista para confirmar la creacion del usuario
def confirm(request):
    return render(request, 'usuarios/confirm.html')


# Controlador para el registro de un Usuario
def createUser(request):
    if request.method == 'POST':
        form = CrearUsuarioForma(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido_paterno = form.cleaned_data['apellido_paterno']
            apellido_materno = form.cleaned_data['apellido_materno']
            telefono = form.cleaned_data['telefono']
            estado = form.cleaned_data['estado']
            nombre_agencia =form.cleaned_data['nombre_agencia']
            numero_agencia = form.cleaned_data['numero_agencia']
            contrasena = form.cleaned_data['contrasena']
            confirmar_contrasena = form.cleaned_data['confirmar_contrasena']
            email = form.cleaned_data['email']

            uname   = nombre[0:2] \
                    + apellido_paterno[0:2] \
                    + apellido_materno[0:2] \
                    + str(TachyonUsuario.objects.all().count()) #crear un username único para el usuario tomando las 2 primeras
                    # letras del nombre y cada apellido más el número de usuarios en el sistema

            # Crear usuario del modelo de django
            u = User.objects.create_user(username=uname, email=email, password=contrasena)

            # Crear usuario de TachyonUsuario
            tUsuario = TachyonUsuario(
                            rol = Rol.objects.get(nombre='Propietario'),
                            user = u,
                            nombre = nombre,
                            apellido_paterno = apellido_paterno,
                            apellido_materno = apellido_materno,
                            telefono = telefono,
                            estado = estado,
                            nombre_agencia = nombre_agencia,
                            numero_agencia = numero_agencia,
                            codigo_registro = randomString(),
            )

            tUsuario.save()
            return redirect('confirm')
        else:
            raise Http404
    else:
        raise Http404


def verificar_correo(request):
    query_mails = User.objects.filter(email=request.POST.get('correo'))
    return JsonResponse({"num_mails": query_mails.count()})


# Funciones extra -------------------------------
# Generar un string aleatorio
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))
