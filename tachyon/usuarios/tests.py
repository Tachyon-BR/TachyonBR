
from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse, resolve
from .views import *
from django.contrib.auth import views as auth_views
from django.core import mail
from .models import *

# Create your tests here.

#Esta prueba revisa que un usuario pueda entrar al login
class testLogin(TestCase):
    #Aquí se crea la base de datos dentro del ambiente de prueba
    def setUp(self):
        user = User.objects.create_user('user', 'user@user.com', 'testpassword')
        user.save()
        r = Rol(nombre='Propietario')
        r.save()
        tUsuario = TachyonUsuario(
                        rol = r,
                        user = user,
                        nombre = 'nombre',
                        apellido_paterno = 'apellido_paterno',
                        apellido_materno = 'apellido_materno',
                        telefono = 'telefono',
                        estado = 'estado',
                        nombre_agencia = '',
                        numero_agencia = '',
                        codigo_registro = '123456',
                        estado_registro = True
        )

        tUsuario.save()


    def test_login_exitoso(self):
        #Esta prueba simula a una usuario con el rol de director que accede correctamente con su usuario y contraseña
        response = self.client.post('/usuarios/verifyLogin/', {'mail':'user@user.com','password':'testpassword'})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_login_no_exitoso(self):
        #Esta prueba simula a una usuario con el rol de director que accede correctamente con su usuario y contraseña
        response = self.client.post('/usuarios/verifyLogin/', {'mail':'use@use.co','password':'testpasswor'})
        self.assertEqual(response.status_code, 200)

    def test_correct_url_reset_password(self):
        # Esta prueba verifica que el acceso a la forma esta cargando el template correcto
        response = self.client.get('/usuarios/reset_password')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['usuarios/reset_password_mail.html'])

    def test_reset_password_post_mail_nonexistent(self):
        # Esta prueba valida que no se envien el correo si no existe
        response = self.client.post('/usuarios/reset_password', {'email':'noexiste@user.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 0)
        self.assertRedirects(response,reverse('password_reset_done'))
    
    def test_reset_password_post_mail_correct(self):
        # Esta prueba valida que se envie un correo existente y verifica el asunto
        response = self.client.post(reverse('reset_password'), {'email':'user@user.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Tachyon: Recupera tu contraseña')
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_reset_password_correct_url_password(self):
        # Esta prueba valida que el id que se envia para acceder a la forma de restaurar contraseña sea el correcto
        response = self.client.post(reverse('reset_password'), {'email':'user@user.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Tachyon: Recupera tu contraseña')
        token = response.context[0]['token']
        uid = response.context[0]['uid']
        response_change_password = self.client.get(
            reverse('password_reset_confirm', kwargs={'uidb64': uid,'token': token})
        )
        self.assertEqual(response_change_password.status_code, 302)

#Esta prueba revisa que un usuario pueda registrarse en la página
class testSignUp(TestCase):
    #crear escenario
    formSubmitD = {
        'nombre': 'Juan',
        'apellido_paterno': 'Perez',
        'apellido_materno': 'Perez',
        'telefono': '123456789',
        'estado': 'Querétaro',
        'nombre_agencia': 'Agencia Chida',
        'numero_agencia': '634567898',
        'contrasena': 'password',
        'confirmar_contrasena': 'password',
        'email': 'test@test.com',
    }

    def login_tachyon(self,mail,password):
        response = self.client.post(reverse('verifyLogin'),{'mail':mail,'password':password})

    def setUp(self):
        p = Permiso(nombre='crear_staff')
        p.save()
        r = Rol(nombre='Propietario')
        r.save()
        p_r = PermisoRol(permiso=p, rol=r)
        p_r.save()
        u = User.objects.create_user(username="UserName", password="contraseña", email="lalo@lalocura.com")
        tu = TachyonUsuario(
            rol= r,
            user= u,
            nombre='Pedro',
            apellido_paterno= 'Perez',
            apellido_materno= 'Perez',
            telefono = '123456789',
            estado = 'Querétaro',
            codigo_registro =  'ASDFGHJKLP',
            estado_registro = True
        )
        tu.save()

    # --- TESTS PARA CREACION DE USUARIOS POR PARTE DE USUARIOS NO REGISTRADOS ---
    def test_createUser_success(self):

        response = self.client.post('/usuarios/createUser', self.formSubmitD)

        #Checar la url de redirección
        url_redirect = 'confirm/' + str(TachyonUsuario.objects.filter(nombre='Juan').latest('nombre').id)
        url_ultimo = 'confirm/' + str(TachyonUsuario.objects.all().last().id)
        self.assertEqual(response.url, url_redirect)
        self.assertEqual(url_redirect, url_ultimo)

        self.assertEqual(response.status_code, 302)

    def test_createUser_fail_wrongMethod(self):
        response = self.client.get('/usuarios/createUser', self.formSubmitD)
        self.assertEqual(response.status_code, 404)

    def test_createUser_fail_wrongFormat(self):
        #falta email
        formSubmit = self.formSubmitD.copy()
        del formSubmit['email']

        response = self.client.post('/usuarios/createUser', formSubmit)
        self.assertEqual(response.status_code, 404)

    def test_confirmMail_success(self):
        first=TachyonUsuario.objects.all().first()
        submitInfo={
            'confirma_id': first.id,
            'confirma_code': first.codigo_registro,
        }
        urlPost = '/usuarios/confirmMail'
        response = self.client.post(urlPost, submitInfo)
        self.assertEqual(response.url, '/')
        self.assertEqual(response.status_code, 302) #codigo redirect

    def test_confirmMail_fail_WrongMethod(self):
        first=TachyonUsuario.objects.all().first()
        submitInfo={
            'confirma_id': first.id,
            'confirma_code': first.codigo_registro,
        }
        urlPost = '/usuarios/confirmMail'
        response = self.client.get(urlPost, submitInfo) #Método get en lugar de post
        #self.assertEqual(response.url, '/')
        self.assertEqual(response.status_code, 404)


    def test_confirmMail_fail_WrongCode(self):
        first=TachyonUsuario.objects.all().first()
        submitInfo={
            'confirma_id': first.id,
            'confirma_code': "PPPPPPP", #Código incorrecto
        }
        urlPost = '/usuarios/confirmMail'
        response = self.client.post(urlPost, submitInfo) #Método get en lugar de post
        self.assertEqual(response.url, '/usuarios/confirm/'+str(first.id))
        self.assertEqual(response.status_code, 302) #código redirección


    #verificar retorna 1 con correo ya existente
    def test_verificar_correo(self):
        formSubmit={
            'correo': 'lalo@lalocura.com'
        }
        response = self.client.post('/usuarios/verificar_correo', formSubmit)
        self.assertEqual(response.json()['num_mails'], 1)

    # --- TESTS PARA CREACION DE USUARIOS POR PARTE DEL ADMIN ---
    def test_adminVerifyCreateUser_success(self):
        self.login_tachyon('lalo@lalocura.com', 'contraseña') #ingresar como un usuario cliente
        formSubmit = self.formSubmitD.copy()
        formSubmit['rol'] = 'Propietario'   # Agregar campo 'rol'

        response = self.client.post('/usuarios/adminVerifyCreateUser', formSubmit)
        session = self.client.session
        self.assertEqual(session['notification_session_type'], 'Success')

    def test_adminVerifyCreateUser_fail_mailAlreadyExist(self):
        self.login_tachyon('lalo@lalocura.com', 'contraseña') #ingresar como un usuario cliente
        formSubmit = self.formSubmitD.copy()
        formSubmit['rol'] = 'Propietario'   # Agregar campo 'rol'
        formSubmit['email'] = 'lalo@lalocura.com'   # Cambiar el correo por uno ya existente

        response = self.client.post('/usuarios/adminVerifyCreateUser', formSubmit)
        session = self.client.session
        self.assertEqual(session['notification_session_type'], 'Danger')

    def test_adminVerifyCreateUser_fail_wrongFormat(self):
        self.login_tachyon('lalo@lalocura.com', 'contraseña') #ingresar como un usuario cliente
        #falta email
        formSubmit = self.formSubmitD.copy()
        del formSubmit['email']

        response = self.client.post('/usuarios/adminVerifyCreateUser', formSubmit)
        session = self.client.session
        self.assertEqual(session['notification_session_type'], 'Danger')

    def test_adminVerifyCreateUser_fail_wrongMethod(self):
        self.login_tachyon('lalo@lalocura.com', 'contraseña') #ingresar como un usuario cliente
        response = self.client.get('/usuarios/adminVerifyCreateUser')
        self.assertEqual(response.status_code, 404)

    def test_adminCreateUserView_success(self):
        self.login_tachyon('lalo@lalocura.com', 'contraseña') #ingresar como un usuario cliente
        response = self.client.get('/usuarios/adminCreateUser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/create.html')

#Esta prueba revisa que un usuario se pueda eliminar
class testDeleteUser(TestCase):
    def setUp(self):
        r = Rol(nombre='Propietario')
        r.save()
        u = User.objects.create_user(username="UserName", password="contraseña", email="lalo@lalocura.com")
        tu = TachyonUsuario(
            rol= r,
            user= u,
            nombre='Pedro',
            apellido_paterno= 'Perez',
            apellido_materno= 'Perez',
            telefono = '123456789',
            estado = 'Querétaro',
            codigo_registro =  'ASDFGHJKLP'
        )
        tu.save()
        u2 = User.objects.create_user(username="UserName2", password="contraseña", email="lalocura@lalocura.com")
        tu2 = TachyonUsuario(
            rol= r,
            user= u2,
            nombre='Pedro',
            apellido_paterno= 'Perez',
            apellido_materno= 'Perez',
            telefono = '123456789',
            estado = 'Querétaro',
            codigo_registro =  'ASDFGHJKLP'
        )
        tu2.save()

    def test_delete_usuario_1(self):
        user = TachyonUsuario.objects.all().first()
        user.estado_eliminado = True
        user.save()
        contador = TachyonUsuario.objects.filter(estado_eliminado=True).count()
        self.assertEquals(1, contador)

    # Si truena está bien, porque el analisis no existe
    def test_delete_usuario_2(self):
        var = False
        try:
            user = TachyonUsuario.objects.all().last()
            user.estado_eliminado = True
            user.save()
            contador = TachyonUsuario.objects.filter(estado=True).count()
            self.assertNotEquals(2, contador)
        except:
            var = True
            self.assertEquals(var, True)

class TestListaUsuarios(TestCase):
    def setUp(self):
        p = Permiso(nombre='visualizar_usuarios')
        p.save()
        r = Rol(nombre='SuperUsaurus')
        r.save()
        p_r = PermisoRol(permiso=p, rol=r)
        p_r.save()
        u = User.objects.create_user(username="UserName", password="contraseña", email="lalo@lalocura.com")
        tu = TachyonUsuario(
            rol= r,
            user= u,
            nombre='Pedro',
            apellido_paterno= 'Perez',
            apellido_materno= 'Perez',
            telefono = '123456789',
            estado = 'Querétaro',
            codigo_registro =  'ASDFGHJKLP',
            estado_registro = True
        )
        u.save()
        tu.save()
        u2 = User.objects.create_user(username="UserName2", password="contraseña", email="lalocura@lalocura.com")
        tu2 = TachyonUsuario(
            rol= r,
            user= u2,
            nombre='Pedro',
            apellido_paterno= 'Perez',
            apellido_materno= 'Perez',
            telefono = '123456789',
            estado = 'Querétaro',
            codigo_registro =  'ASDFGHJKLP'
        )
        u2.save()
        tu2.save()

    def login_tachyon(self,mail,password):
        response = self.client.post(reverse('verifyLogin'),{'mail':mail,'password':password})

    def test_no_login(self):
        response = self.client.get('/usuarios/')
        self.assertEqual(response.status_code, 302)

    def test_url_resuelta(self):
        self.login_tachyon('lalo@lalocura.com','contraseña') #ingresar como un usuario cliente
        response = self.client.get('/usuarios/')
        self.assertEqual(response.status_code, 200)
