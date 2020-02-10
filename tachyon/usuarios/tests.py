
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .views import *
from django.contrib.auth import views as auth_views
from django.core import mail

# Create your tests here.
"""
#Esta prueba revisa que un usuario pueda entrar al login
class testLogin(TestCase):
    #Aquí se crea la base de datos dentro del ambiente de prueba
    def setUp(self):
        user = User.objects.create_user('user', 'user@user.com', 'testpassword')
        user.save()

    def test_login_exitoso(self):
        #Esta prueba simula a una usuario con el rol de director que accede correctamente con su usuario y contraseña
        response = self.client.post('/usuarios/verifyLogin/', {'mail':'user@user.com','password':'testpassword'})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_login_no_exitoso(self):
        #Esta prueba simula a una usuario con el rol de director que accede correctamente con su usuario y contraseña
        response = self.client.post('/usuarios/verifyLogin/', {'mail':'use@use.co','password':'testpasswor'})
        self.assertEqual(response.status_code, 200)
"""

#Esta prueba revisa que un usuario pueda registrarse en la página
class testSignUp(TestCase):
    #crear escenario
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

    def test_createUser_success(self):
        formSubmit = {
            'nombre': 'Juan',
            'apellido_paterno': 'Perez',
            'apellido_materno': 'Perez',
            'telefono': '123456789',
            'estado': 'Querétaro',
            'nombre_agencia': 'Agencia Chida',
            'numero_agencia': '634567898',
            'contrasena': 'password',
            'confirmar_contrasena': 'password',
            'email': 'dantemaxflores@gmail.com',
        }
        response = self.client.post('/usuarios/createUser', formSubmit)
        
        #Checar la url de redirección
        url_redirect = 'confirm/' + str(TachyonUsuario.objects.filter(nombre='Juan').latest('nombre').id)
        url_ultimo = 'confirm/' + str(TachyonUsuario.objects.all().last().id)
        self.assertEqual(response.url, url_redirect) 
        self.assertEqual(url_redirect, url_ultimo) 
        
        self.assertEqual(response.status_code, 302)

    def test_createUser_fail_wrongMethod(self):
        formSubmit = {
            'nombre': 'Juan',
            'apellido_paterno': 'Perez',
            'apellido_materno': 'Perez',
            'telefono': '123456789',
            'estado': 'Querétaro',
            'nombre_agencia': 'Agencia Chida',
            'numero_agencia': '634567898',
            'contrasena': 'password',
            'confirmar_contrasena': 'password',
            'email': 'asdasd_asd@asd.com',
        }
        response = self.client.get('/usuarios/createUser', formSubmit)
        self.assertEqual(response.status_code, 404)

    def test_createUser_fail_wrongFormat(self):
        #falta email
        formSubmit = {
            'nombre': 'Juan',
            'apellido_paterno': 'Perez',
            'apellido_materno': 'Perez',
            'telefono': '123456789',
            'estado': 'Querétaro',
            'nombre_agencia': 'Agencia Chida',
            'numero_agencia': '634567898',
            'contrasena': 'pword',
            'confirmar_contrasena': 'pword',
        }
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
        self.assertEqual(response.url, '/usuarios/confirm/1')
        self.assertEqual(response.status_code, 302) #código redirección 


    #verificar retorna 1 con correo ya existente
    def test_verificar_correo(self):
        formSubmit={
            'correo': 'lalo@lalocura.com'
        }
        response = self.client.post('/usuarios/verificar_correo', formSubmit)    
        self.assertEqual(response.json()['num_mails'], 1)