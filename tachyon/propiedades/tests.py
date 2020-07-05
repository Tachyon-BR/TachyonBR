from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse, resolve
from .views import *
from django.contrib.auth import views as auth_views
from django.core.files import File

import unittest
from unittest import mock


# Create your tests here.


#Esta prueba revisa que un usuario pueda entrar al login
class testRevisores(TestCase):
    #Aquí se crea la base de datos dentro del ambiente de prueba
    #crear usuario propietario y su propiedad, usuario revisor
    def setUp(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test.png'

        p = Permiso(nombre='visualizar_peticiones')
        p.save()
        r = Rol(nombre='Revisor')
        r.save()
        p_r = PermisoRol(permiso=p, rol=r)
        p_r.save()
        p = Permiso(nombre='seleccionar_peticion')
        p.save()
        p_r = PermisoRol(permiso=p, rol=r)
        p_r.save()
        
        user = User.objects.create_user('user', 'user@user.com', 'testpassword')
        user.save()
        r_prop = Rol(nombre='Propietario')
        r_prop.save()
        tUsuario = TachyonUsuario(
                        rol = r_prop,
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

        #propiedad en revisión
        prop = Propiedad(
            propietario = tUsuario,
            titulo = "a",
            tipo = "a",
            oferta = "a",
            descripcion = "a",
            metros_terreno = 10,
            metros_construccion = 10,
            pais = "a",
            codigo_postal = 123,
            estado = "a",
            colonia = "a",
            direccion = "a",
            precio = 10,
            negociable = True,
            estado_revision = True,
            portada = file_mock

        )
        prop.save()

        #propiedad no en revisión
        prop = Propiedad(
            propietario = tUsuario,
            titulo = "a",
            tipo = "a",
            oferta = "a",
            descripcion = "a",
            metros_terreno = 10,
            metros_construccion = 10,
            pais = "a",
            codigo_postal = 123,
            estado = "a",
            colonia = "a",
            direccion = "a",
            precio = 10,
            negociable = True,
            estado_revision = False,
            portada = file_mock
        )
        prop.save()

        user_revisor = User.objects.create_user('user_revisor', 'lalo@lalocura.com', 'contraseña')
        user_revisor.save()
        tUsuario_revisor = TachyonUsuario(
                        rol = r,
                        user = user_revisor,
                        nombre = 'nombre_revisor',
                        apellido_paterno = 'apellido_paterno',
                        apellido_materno = 'apellido_materno',
                        telefono = 'telefono',
                        estado = 'estado',
                        nombre_agencia = '',
                        numero_agencia = '',
                        codigo_registro = '123456',
                        estado_registro = True
        )

        tUsuario_revisor.save()

    def login_tachyon(self,mail,password):
        response = self.client.post(reverse('verifyLogin'),{'mail':mail,'password':password})


 

    def test_ver_en_revision_rol_correcto(self):
        #Simula alguien entrando a revisiones con rol correcto
        self.login_tachyon('lalo@lalocura.com','contraseña') #ingresar como un usuario revisor
        response = self.client.get('/propiedades/enRevision/', {}, follow=True)
        self.assertEquals(response.status_code, 200)

        
    def test_ver_en_revision_rol_incorrecto(self):
        #Simula alguien entrando a revisiones con rol incorrecto
        self.login_tachyon('user@user.com','testpassword') #ingresar como un usuario revisor
        response = self.client.get('/propiedades/enRevision/', follow=True)
        self.assertEqual(response.status_code, 404)

    """
    def test_ver_en_revision_no_login(self):
        #Simula alguien entrando a revisiones sin logearse
        response = self.client.get('/propiedades/enRevision/', follow=True)
        print(response.status_code)
        self.assertEquals(response.status_code, 404)
    """

    # PRUEBAS DEL REVISOR INTENTANDOSE AGREGAR A PROPIEDADES COMO REVISOR -----

    # se agrega a una propiedad que existe y estatus es en revision
    def test_agregarse_revisor_propiedad_correcto(self):
        self.login_tachyon('lalo@lalocura.com','contraseña') #ingresar como un usuario revisor
        response = self.client.post('/propiedades/addRevisor/', {'id_prop' : 1}, follow=True)
        self.assertEqual(response.status_code, 200)

    # envía un post sin data
    def test_agregarse_revisor_propiedad_sin_data_error(self):
        self.login_tachyon('lalo@lalocura.com','contraseña') #ingresar como un usuario revisor
        response = self.client.post('/propiedades/addRevisor/', follow=True)
        self.assertEqual(response.status_code, 400)

    # se busca un id que no existe
    def test_agregarse_revisor_propiedad_id_no_existe_error(self):
        self.login_tachyon('lalo@lalocura.com','contraseña') #ingresar como un usuario revisor
        response = self.client.post('/propiedades/addRevisor/', {'id_prop' : 7}, follow=True)
        self.assertEqual(response.status_code, 400)

    # se agrega a una propiedad que no está en revisión
    def test_agregarse_revisor_propiedad_prop_no_enrevision_error(self):
        self.login_tachyon('lalo@lalocura.com','contraseña') #ingresar como un usuario revisor
        response = self.client.post('/propiedades/addRevisor/', {'id_prop': 2}, follow=True)
        self.assertEqual(response.status_code, 400)

    # se agrega a una propiedad que ya tiene revisor
    def test_agregarse_revisor_propiedad_revisor_ya_asignado_error(self):
        self.login_tachyon('lalo@lalocura.com','contraseña') #ingresar como un usuario revisor
        response1 = self.client.post('/propiedades/addRevisor/', {'id_prop' : 1}, follow=True)
        response2 = self.client.post('/propiedades/addRevisor/', {'id_prop' : 1}, follow=True)
        self.assertEqual(response2.status_code, 400)

    """
    # entra a agregarse sin logearse
    def test_agregarse_revisor_propiedad_no_login_error(self):
        response = self.client.post('/propiedades/addRevisor/', {'id_prop' : 1}, follow=True)
        print(response.status_code)
        self.assertEquals(response.status_code, 404)
    """
    
    # entra a agregarse con usuario que no tiene rol correcto
    def test_agregarse_revisor_propiedad_rol_incorrecto(self):
        self.login_tachyon('user@user.com','testpassword') #ingresar como un usuario propietario
        response = self.client.post('/propiedades/addRevisor/', {'id_prop' : 7}, follow=True)
        self.assertEqual(response.status_code, 404)

