from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Modelo de roles
class Rol(models.Model):
    nombre = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return "%s" % (self.nombre,)


# Modelo de los usuarios de Tachyon
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
    status = models.BooleanField(default = True)        # Utilizado para verificar si la cuenta fue borrada o no
    nombre_agencia = models.CharField(max_length = 500, null=True, blank=True)
    numero_agencia = models.CharField(max_length = 500, null=True, blank=True)
    codigo_registro = models.CharField(max_length = 10) # Utilizado para verificar el correo electrónico
    estado = models.CharField(max_length = 500, null=True, blank=True)
    estado_registro = models.BooleanField(default = False)             # Utilizado para validar si el correo fue verificado
    estado_eliminado = models.BooleanField(default = False)             # Utilizado para validar si el usuario fue eliminado

    class Meta:
        verbose_name = 'Usuario de Tachyon'
        verbose_name_plural = 'Usuarios de Tachyon'

    def __str__(self):
        return "%s %s %s" % (self.id, self.nombre, self.apellido_paterno)


# Modelos de los permisos de usuario
class Permiso(models.Model):
    idPermiso =  models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 50)

    class Meta:
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

    def _str_(self):
        return "%s" % (self.nombre)


# Modelo de tabla de relacion N a N
class PermisoRol(models.Model):
    idPermisoRol = models.AutoField(primary_key=True)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Permiso Rol'
        verbose_name_plural = 'Permiso Roles'

    def _str_(self):
        return "%s %s" % (self.permiso.nombre, self.rol.nombre)
