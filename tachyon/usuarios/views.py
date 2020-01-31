from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core import serializers
from django.urls import reverse
from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

# Create your views here.

def create(request):
    return render(request, 'usuarios/create.html')

def confirm(request):
    return render(request, 'usuarios/confirm.html')

#Vista de login
def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'usuarios/login.html')

#Controlador login
def verifyLogin(request):
    mail = request.POST['mail']
    password = request.POST['password']
    try:
        username = User.objects.get(email=mail.lower()).username
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # ifc_user = IFCUsuario.objects.get(user = request.user)
            # request.session['username'] = ifc_user.nombre
            # request.session['userrole'] = ifc_user.rol.nombre
            # permissions = PermisoRol.objects.all().filter(rol=ifc_user.rol)
            # list_permissions = []
            # for permission in permissions:
            #     list_permissions.append(permission.permiso.nombre)
            # request.session['permissions'] = list_permissions
            return redirect('/')
        else:
            #Redireccionar error
            return render(request,'usuarios/login.html', {
                'error': 'Tu correo o contraseña está incorrecto. Verifica tus credenciales para iniciar sesión.'
            })
    except:
        #Redireccionar error
        return render(request,'usuarios/login.html', {
            'error': 'Tu correo o contraseña está incorrecto. Verifica tus credenciales para iniciar sesión.'
        })
        return 0

#Controlador logout
def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return render(request, 'usuarios/login.html')

# def loggedOut(request):
#     # Funcion encargada de mostar la vista para
#     return render(request,'cuentas/login.html', {
#         'success': 'Sesión cerrada correctamente'
#     })
