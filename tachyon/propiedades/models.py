from django.db import models
from .models import *
from usuarios.models import *

# Create your models here.

def path_portada(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/property_{1}/main/{2}'.format(instance.propietario.pk, instance.pk, filename)

def path_imagenes(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/property_{1}/extra/{2}'.format(instance.propietario.pk, instance.pk, filename)

# Modelo de los usuarios de Tachyon
class Propiedad(models.Model):
    # Llave foranea del rol al que pertenece
    propietario = models.ForeignKey(TachyonUsuario, on_delete=models.CASCADE)
    # Campos adicionales
    titulo = models.CharField(max_length = 200)
    tipo = models.CharField(max_length = 100)
    oferta = models.CharField(max_length = 100)
    descripcion = models.TextField()
    habitaciones = models.PositiveSmallIntegerField(null=True, blank=True)
    banos = models.FloatField(null=True, blank=True)
    garaje = models.PositiveSmallIntegerField(null=True, blank=True)
    metros_terreno = models.FloatField()
    metros_construccion = models.FloatField()
    pais = models.CharField(max_length = 100)
    codigo_postal = models.IntegerField()
    estado = models.CharField(max_length = 100)
    colonia = models.CharField(max_length = 200)
    direccion = models.CharField(max_length = 300)
    precio = models.FloatField()
    pisos = models.PositiveSmallIntegerField(null=True, blank=True)
    estado_activo = models.BooleanField(default = False)
    visitas = models.IntegerField()
    fecha_creacion = models.DateField(auto_now = True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    fecha_corte = models.DateField(null=True, blank=True)
    portada = models.ImageField(upload_to = path_portada, null=True, blank=True)
    negociable = models.BooleanField()
    diferenciador = models.CharField(max_length = 100)
    video = models.CharField(max_length = 150)

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'

    def __str__(self):
        return "%s" % (self.titulo)


# Modelo de tabla de relacion 1 a N
class Foto(models.Model):
    # Llave foranea del rol al que pertenece
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    # Campos adicionales
    imagen = models.ImageField(upload_to = path_imagenes)
    orden = models.PositiveSmallIntegerField()
    fecha = models.DateField(auto_now = True)

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'

    def __str__(self):
        return "%s %s" % (self.propiedad.pk, self.pk)


class CodigoPostal(models.Model):
    codigo = models.CharField(max_length = 5)
    asenta = models.CharField(max_length = 100)
    tipo_asenta = models.CharField(max_length = 100)
    municipio = models.CharField(max_length = 100)
    estado = models.CharField(max_length = 100)
    ciudad = models.CharField(max_length = 100)
    CP = models.IntegerField(null=True, blank=True)
    c_estado = models.IntegerField(null=True, blank=True)
    c_oficina = models.IntegerField(null=True, blank=True)
    c_CP = models.IntegerField(null=True, blank=True)
    c_tipo_asenta = models.IntegerField(null=True, blank=True)
    c_mnpio = models.IntegerField(null=True, blank=True)
    id_asenta_cpcons = models.IntegerField(null=True, blank=True)
    d_zona = models.CharField(max_length = 100, null=True, blank=True)
    c_cve_ciudad = models.IntegerField(null=True, blank=True)
