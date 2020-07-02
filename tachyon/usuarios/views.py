from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from .forms import CrearUsuarioForma
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
import time
import string
from .models import *
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.http import HttpResponse

# Create your views here.

# Vista de registro de Usuarios
def create(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'usuarios/create.html')


#Vista de login
def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'usuarios/login.html')

#Controlador login
def verifyLogin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        mail = request.POST['mail']
        password = request.POST['password']
        try:
            username = User.objects.get(email=mail.lower()).username
            user = authenticate(request, username=username, password=password)
            tachyon_user = TachyonUsuario.objects.get(user = User.objects.get(username=username))

            if user is not None:
                if not tachyon_user.estado_registro:
                    return redirect('/usuarios/confirm/'+str(tachyon_user.id))

                if tachyon_user.estado_eliminado:
                    return render(request,'usuarios/login.html', {
                        'warning': 'Tu cuenta se encuentra temporalmente suspendida, comunícate con el equipo de Tachyon para más información.'
                    })

                login(request, user)
                t_user = TachyonUsuario.objects.get(user = request.user)
                request.session['username'] = t_user.nombre
                request.session['userrole'] = t_user.rol.nombre
                permissions = PermisoRol.objects.all().filter(rol=t_user.rol)
                list_permissions = []
                for permission in permissions:
                    list_permissions.append(permission.permiso.nombre)
                request.session['permissions'] = list_permissions
                return redirect('/')
            else:
                #Redireccionar error
                return render(request,'usuarios/login.html', {
                    'error': 'Tu correo o contraseña está incorrecto. Verifica tus credenciales para iniciar sesión.'
                })
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            #print (message)
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
        return redirect('/')


# Vista para confirmar la creacion del usuario
def confirm(request, id):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        tu = TachyonUsuario.objects.filter(id=id)

        if len(tu) == 0:
            raise Http404

        if tu.first().estado_registro:  # Verificar si la cuenta ya fue verificada
            return redirect('/')

        mail = tu.first().user.email

        if request.session.get('error_confirm'):            # Verifica que la variable de sesion exista
            error_msg = request.session['error_confirm']    # Enviar el mensaje de error a una variable de contexto
            del request.session['error_confirm']
        else:
            error_msg = ''

        context = {
            'mail' : mail,
            'id': id,
            'error' : error_msg
        }
        return render(request, 'usuarios/confirm.html', context)


# Controlador para el registro de un Usuario
def createUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
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


                checkEmail = User.objects.filter(email=email)
                if(len(checkEmail)>0):
                    request.session['notification_session_msg'] = "El correo ya existe."
                    request.session['notification_session_type'] = "Danger"
                    return redirect('/usuarios/create')

                uname   = nombre[0:2] \
                        + apellido_paterno[0:2] \
                        + apellido_materno[0:2] \
                        + str(TachyonUsuario.objects.all().count()) #crear un username único para el usuario tomando las 2 primeras
                        # letras del nombre y cada apellido más el número de usuarios en el sistema

                # Crear usuario del modelo de django
                u = User.objects.create_user(username=uname, email=email.lower(), password=contrasena)

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
                if (email != 'test@test.com'):
                    # Enviar correo con codigo de registro
                    message = Mail(
                        from_email='tachyon.icarus@gmail.com',
                        to_emails=email,
                        subject='Verificacion de registro a Tachyon',
                        html_content='<p>Gracias por registrarte a Tachyon B.R. [Nombre sujeto a cambios]</p><p>Tu código de verificación es el siguiente: <strong>'+tUsuario.codigo_registro+'</strong></p>')
                    try:
                        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                        response = sg.send(message)
                        print(response.status_code)
                        print(response.body)
                        print(response.headers)
                    except Exception as e:
                        print(e)

                return redirect('confirm/'+str(tUsuario.id))
            else:
                raise Http404
        else:
            raise Http404


# Vista consultada con AJAX
def verificar_correo(request):
    query_mails = User.objects.filter(email=request.POST.get('correo'))
    return JsonResponse({"num_mails": query_mails.count()})


def confirmMail(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            id = request.POST['confirma_id']
            code = request.POST['confirma_code']

            tu = TachyonUsuario.objects.filter(id=id)

            if len(tu) == 0:
                raise Http404

            user_to_verify = tu.first()

            if (user_to_verify.codigo_registro == code):
                user_to_verify.estado_registro = True
                user_to_verify.save()
                request.session['notification_session_msg'] = "Se ha verificado tu cuenta correctamente. Ya puedes iniciar sesión."
                request.session['notification_session_type'] = "Success"
                return redirect('/')
            else:
                request.session['error_confirm'] = 'El código de verificación es incorrecto.'
                return redirect('/usuarios/confirm/'+str(id))

        else:
            raise Http404

# Funciones extra -------------------------------
# Generar un string aleatorio
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))


@login_required
#Controlador para lista de usuarios
def indexView(request):
    if 'visualizar_usuarios' in request.session['permissions']:
        tachyons = TachyonUsuario.objects.all().exclude(user = request.user)

        context = {
            'tachyons': tachyons
        }

        return render(request, 'usuarios/users.html', context)
    else:
        raise Http404

def deleteUserView(request, id):
    if 'eliminar_usuario' in request.session['permissions']:
        if request.method == 'POST':
            user = TachyonUsuario.objects.filter(pk = id).first()
            if user:
                user.estado_eliminado = not user.estado_eliminado
                user.save()
                return HttpResponse('OK')
            else:
                response = JsonResponse({"error": "No existe ese usuario"})
                response.status_code = 500
                # Regresamos la respuesta de error interno del servidor
                return response
        else:
            response = JsonResponse({"error": "No se mandó por el método correcto"})
            response.status_code = 500
            # Regresamos la respuesta de error interno del servidor
            return response
    else: # Si el rol del usuario no es ventas no puede entrar a la página
        raise Http404


# Vista para registrar usuario por parte de admin
@login_required
def adminCreateUserView(request):
    if 'crear_staff' in request.session['permissions']:
        context = {
            'adminCreator': True
        }
        return render(request, 'usuarios/create.html', context)
    else: # Si el rol del usuario no es ventas no puede entrar a la página
        raise Http404

@login_required
def adminVerifyCreateUser(request):
    if 'crear_staff' in request.session['permissions']:
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
                rol = form.cleaned_data['rol']


                checkEmail = User.objects.filter(email=email)
                if(len(checkEmail)>0):
                    request.session['notification_session_msg'] = "El correo ya existe."
                    request.session['notification_session_type'] = "Danger"
                    return redirect('/usuarios/adminCreateUserView')

                uname   = nombre[0:2] \
                        + apellido_paterno[0:2] \
                        + apellido_materno[0:2] \
                        + str(TachyonUsuario.objects.all().count()) #crear un username único para el usuario tomando las 2 primeras
                        # letras del nombre y cada apellido más el número de usuarios en el sistema

                # Crear usuario del modelo de django
                u = User.objects.create_user(username=uname, email=email.lower(), password=contrasena)

                # Crear usuario de TachyonUsuario
                tUsuario = TachyonUsuario(
                                rol = Rol.objects.get(nombre=rol),
                                user = u,
                                nombre = nombre,
                                apellido_paterno = apellido_paterno,
                                apellido_materno = apellido_materno,
                                telefono = telefono,
                                estado = estado,
                                nombre_agencia = nombre_agencia,
                                numero_agencia = numero_agencia,
                                codigo_registro = randomString(),
                                estado_registro = True
                )

                tUsuario.save()
                if (email != 'test@test.com'):
                    # Enviar correo con codigo de registro
                    message = Mail(
                        from_email='tachyon.icarus@gmail.com',
                        to_emails=email,
                        subject='Bienvenido a Tachyon',
                        html_content='<p>Saludos '+nombre+'. </p>\
                            <p>¡Ya eres miembro de Tachyon B.R.!</p>\
                            <p>Tus datos para iniciar sesión son los siguientes: </p>\
                            <ul>\
                            <li>Correo: <strong>'+email.lower()+'</strong></li>\
                            <li>Contraseña: <strong>'+contrasena+'</strong></li>\
                            </ul>')
                    try:
                        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                        response = sg.send(message)
                        print(response.status_code)
                        print(response.body)
                        print(response.headers)
                    except Exception as e:
                        print(e)

                request.session['notification_session_msg'] = "Se ha creado la cuenta de manera exitosa."
                request.session['notification_session_type'] = "Success"
                return redirect('/usuarios/')
            else:
                # Si la forma no es válida
                request.session['notification_session_msg'] = "Ha ocurrido un error. Inténtelo de nuevo más tarde."
                request.session['notification_session_type'] = "Danger"
                return redirect('/usuarios/')
        else:
            # Si no se utiliza el metodo POST
            raise Http404
    else: # Si el rol del usuario no es ventas no puede entrar a la página
        raise Http404

def getLoggedUserJson(request):
    user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
    data = serializers.serialize('json', user_logged)
    return JsonResponse({"user": data})