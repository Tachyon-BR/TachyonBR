from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from django.urls import reverse, resolve
from .views import *
from django.contrib.auth import views as auth_views
from django.core import mail
from .models import *

# Create your tests here.
class testProperty(TestCase):
    #Aquí se crea la base de datos dentro del ambiente de prueba
    def login_tachyon(self,mail,password):
        response = self.client.post(reverse('verifyLogin'),{'mail':mail,'password':password})

    def setUp(self):
        user = User.objects.create_user('user', 'user@user.com', 'testpassword')
        user.save()
        p = Permiso(nombre='eliminar_propiedad')
        p.save()
        r = Rol(nombre='Propietario')
        r.save()
        p_r = PermisoRol(permiso=p, rol=r)
        p_r.save()
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

        user2 = User.objects.create_user('user2', 'user2@user.com', 'testpassword2')
        user2.save()
 
        tUsuario2 = TachyonUsuario(
                        rol = r,
                        user = user2,
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
        tUsuario2.save()

        prop = Propiedad(
            propietario = tUsuario,
            titulo = 'Test',
            tipo = 'Test',
            oferta = 'Test',
            descripcion = 'More test',
            metros_terreno = 10.0,
            metros_construccion = 10.0,
            pais = 'Mexico',
            codigo_postal = 4561,
            estado = 'Test',
            colonia = 'Test',
            direccion = 'Test',
            precio = 1000000.0,
            negociable = True,
        )

        prop.save()
    
    def test_eliminar_get(self):
        # Esta prueba intenta borrar una propiedad mediante un GET
        self.login_tachyon('user@user.com', 'testpassword')
        p = Propiedad.objects.get(titulo='Test')
        response = self.client.get('/propiedades/deleteProperty/'+str(p.pk))
        self.assertEqual(response.status_code, 500)

    def test_eliminar_ajeno(self):
        # Esta prueba intenta borrar una propiedad ajena al usuario
        self.login_tachyon('user2@user.com', 'testpassword2')
        p = Propiedad.objects.get(titulo='Test')
        response = self.client.post('/propiedades/deleteProperty/'+str(p.pk))
        self.assertEqual(response.status_code, 401)

    def test_eliminar_success(self):
        # Esta prueba intenta borrar una propiedad mediante un GET   
        self.login_tachyon('user@user.com', 'testpassword')
        p = Propiedad.objects.get(titulo='Test')
        response = self.client.post('/propiedades/deleteProperty/'+str(p.pk))
        self.assertEqual(response.status_code, 200)