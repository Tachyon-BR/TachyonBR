from django.test import TestCase
from django.contrib.auth.models import User
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
        rol = Rol()
        rol.nombre = "Propietario"
        rol.save()
        tachyon = TachyonUsuario()
        tachyon.rol = rol
        tachyon.user = user
        tachyon.estado_registro = True
        tachyon.save()

    def test_login_exitoso(self):
        #Esta prueba simula a una usuario con el rol de director que accede correctamente con su usuario y contraseña
        response = self.client.post('/usuarios/verifyLogin/', {'mail':'user@user.com','password':'testpassword'})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_login_no_exitoso(self):
        #Esta prueba simula a una usuario con el rol de director que accede correctamente con su usuario y contraseña
        response = self.client.post('/usuarios/verifyLogin/', {'mail':'use@use.co','password':'testpasswor'})
        self.assertEqual(response.status_code, 200)
