from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Modelo de roles
class Rol(models.Model):
    nombre = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def _str_(self):
        return "%s" % (self.nombre,)


class TachyonUsuario(models.Model):
    # Llave foranea del rol al que pertenece
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    # Relacion uno a uno con User de Django
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Campos adicionales
    nombre = models.CharField(max_length = 30)
    apellido_paterno = models.CharField(max_length = 30)
    apellido_materno = models.CharField(max_length = 30)
    telefono = models.CharField(max_length = 15)
    estado = models.BooleanField(default = True)
    nombre_agencia = models.CharField(max_length = 500)
    numero_agencia = models.CharField(max_length = 500)
    codigo_registro = models.CharField(max_length = 10)
