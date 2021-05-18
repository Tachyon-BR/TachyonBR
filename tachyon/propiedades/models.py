from django.db import models
from .models import *
from usuarios.models import *
from django.contrib.postgres.fields import ArrayField

# Create your models here.

def path_portada(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/property_{1}/main/{2}'.format(instance.propietario.pk, instance.pk, filename)

def path_imagenes(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/property_{1}/extra/{2}'.format(instance.propiedad.propietario.pk, instance.propiedad.pk, filename)

def path_temp(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/temp/{1}'.format(instance.propietario.pk, filename)

class FB_Page(models.Model):
    page_id = models.CharField(max_length = 500, null=True, blank=True)
    access_token = models.CharField(max_length = 500, null=True, blank=True)
    link_url = models.CharField(max_length = 500, null=True, blank=True)
    expires_in = models.IntegerField(null=True, blank=True)

# Modelo de los usuarios de Tachyon
class Propiedad(models.Model):
    # Llave foranea del rol al que pertenece
    propietario = models.ForeignKey(TachyonUsuario, on_delete=models.CASCADE)
    revisor = models.ForeignKey(TachyonUsuario, on_delete=models.SET_NULL, blank=True, null=True, related_name='revisor_propiedad')
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
    visitas = models.IntegerField(default = 0)
    fecha_creacion = models.DateField(auto_now_add = True)
    fecha_modificacion = models.DateField(auto_now = True)
    fecha_publicacion = models.DateField(null=True, blank=True)
    fecha_corte = models.DateField(null=True, blank=True)
    portada = models.ImageField(upload_to = path_portada, null=True, blank=True)
    negociable = models.BooleanField()
    diferenciador = models.CharField(max_length = 100, null=True, blank=True)
    video = models.CharField(max_length = 150, null=True, blank=True)
    estado_revision = models.BooleanField(default = False)
    estado_visible = models.BooleanField(default = True)
    otros = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    restricciones = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    fb_id = models.CharField(max_length = 500, null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            this = Propiedad.objects.get(id=self.id)
            if this.portada != self.portada:
                this.portada.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'

    def __str__(self):
        return "%s" % (self.titulo)



class PropiedadComentario(models.Model):
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    comentario = models.CharField(max_length = 500)
    fecha = models.DateTimeField(auto_now_add = True)
    revisor = models.ForeignKey(TachyonUsuario, on_delete=models.CASCADE)

    class Meta:
       ordering = ('fecha',)


def path_marcaAgua(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'marca_agua/{0}'.format(filename)


class MARCA_AGUA(models.Model):
    imagen = models.ImageField(upload_to = path_marcaAgua)



# Modelo de tabla de relacion 1 a N
class Foto(models.Model):
    # Llave foranea del rol al que pertenece
    propiedad = models.ForeignKey(Propiedad, on_delete=models.CASCADE)
    # Campos adicionales
    imagen = models.ImageField(upload_to = path_imagenes)
    orden = models.PositiveSmallIntegerField()
    fecha_creacion = models.DateField(auto_now_add = True)
    fecha_modificacion = models.DateField(auto_now = True)

    def save(self, *args, **kwargs):
        try:
            this = Foto.objects.get(id=self.id)
            if this.imagen != self.imagen:
                this.imagen.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)

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
    ciudad = models.CharField(max_length = 100, null=True, blank=True)
    d_CP = models.IntegerField(null=True, blank=True)
    c_estado = models.IntegerField(null=True, blank=True)
    c_oficina = models.IntegerField(null=True, blank=True)
    c_CP = models.IntegerField(null=True, blank=True)
    c_tipo_asenta = models.IntegerField(null=True, blank=True)
    c_mnpio = models.IntegerField(null=True, blank=True)
    id_asenta_cpcons = models.IntegerField(null=True, blank=True)
    d_zona = models.CharField(max_length = 100, null=True, blank=True)
    c_cve_ciudad = models.IntegerField(null=True, blank=True)


# Modelo de tabla de relacion 1 a N
class Temp(models.Model):
    # Llave foranea del rol al que pertenece
    propietario = models.ForeignKey(TachyonUsuario, on_delete=models.CASCADE)
    # Campos adicionales
    imagen = models.ImageField(upload_to = path_temp)
    orden = models.PositiveSmallIntegerField()
    fecha_creacion = models.DateField(auto_now_add = True)
    fecha_modificacion = models.DateField(auto_now = True)
    activo = models.BooleanField(default = True)

    def save(self, *args, **kwargs):
        try:
            this = Temp.objects.get(id=self.id)
            if this.imagen != self.imagen:
                this.imagen.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Temp'
        verbose_name_plural = 'Temps'

    def __str__(self):
        return "%s %s" % (self.propietario.pk, self.pk)
