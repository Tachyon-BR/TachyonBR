from PIL import Image
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.http import Http404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
import time
import string
from .models import *
import os
from django.http import HttpResponse
import datetime
from .forms import *
from django.core.serializers.json import DjangoJSONEncoder
import locale
from django.db.models import Q # new
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
import calendar
from django.core.files import File


# Create your views here.

#Esta clase sirve para serializar los objetos de los modelos.
class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cotizacion):
            return str(obj)
        return super().default(obj)

# Vista de una Propiedad
def propertyView(request, id):
    propiedad = Propiedad.objects.filter(pk = id).first()
    if propiedad:
        if not propiedad.estado_visible:
            return HttpResponseRedirect(reverse('home'))
        if request.user.is_anonymous:
            if not propiedad.estado_activo:
                return HttpResponseRedirect(reverse('home'))
            propiedad.visitas = propiedad.visitas + 1
            propiedad.save()
        else:
            user_logged = TachyonUsuario.objects.get(user = request.user)
            if propiedad.estado_activo:
                if propiedad.propietario != user_logged and user_logged.rol.nombre == 'Propietario':
                    propiedad.visitas = propiedad.visitas + 1
                    propiedad.save()
            else:
                if propiedad.propietario != user_logged and user_logged.rol.nombre == 'Propietario':
                    return HttpResponseRedirect(reverse('home'))
        revisor = False

        fotos = Foto.objects.filter(propiedad = id)
        fotos = fotos.order_by('orden')

        link = propiedad.video
        index = -1
        if link:
            index = link.find('watch?v=')
            if index != -1:
                link = link[0:index] + 'embed/' + link[index + 8:len(link)]
        if propiedad.revisor:
            if request.user.is_authenticated:
                user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
                if propiedad.revisor == user_logged:
                    if propiedad.estado_revision:
                        revisor = True

        is_revisor = False
        if not request.user.is_anonymous:
            if propiedad.revisor:
                userloggednow = TachyonUsuario.objects.get(user = request.user)
                rol = userloggednow.rol.nombre
                revisorparaarriba= ["SuperAdministrador", "Administrador", "SuperUsaurus"]
                if rol in revisorparaarriba:
                    is_revisor = True
                if userloggednow.pk == propiedad.revisor.pk:
                    is_revisor = True
            if propiedad.estado_activo:
                userloggednow = TachyonUsuario.objects.get(user = request.user)
                rol = userloggednow.rol.nombre
                revisorparaarriba= ["SuperAdministrador", "Administrador", "SuperUsaurus"]
                if rol in revisorparaarriba:
                    is_revisor = True

        otros = propiedad.otros
        ofirst = []
        olast = []
        if otros:
            bool = True
            for o in otros:
                if bool:
                    ofirst.append(o)
                else:
                    olast.append(o)
                bool = not bool

        rest = propiedad.restricciones
        rfirst = []
        rlast = []
        if rest:
            bool = True
            for r in rest:
                if bool:
                    rfirst.append(r)
                else:
                    rlast.append(r)
                bool = not bool

        return render(request, 'propiedades/property.html', {'property': propiedad, 'images': fotos, 'link': link, 'index': index, 'revisor': revisor, 'is_revisor': is_revisor, 'ofirst': ofirst, 'olast': olast, 'rfirst': rfirst, 'rlast': rlast, 'property_meta': True})
    else:
        raise Http404

def is_valid_queryparam(param):
    return param is not None and param != ''

# Vista de las Propiedades
def indexView(request):

    class ActiveFilter():
        def __init__(self, text, attr, val = None):
            self.text = text
            self.attr = attr
            self.val = val

    resultados = Propiedad.objects.filter(estado_activo = True)
    tipo = request.GET.get('tipo')
    oferta = request.GET.get('oferta')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    estado = request.GET.get('estado')
    habitaciones = request.GET.get('habitaciones')
    metros_terreno = request.GET.get('metros_terreno')
    metros_construccion = request.GET.get('metros_construccion')
    banos = request.GET.get('banos')
    pisos = request.GET.get('pisos')
    garage = request.GET.get('garage')
    orden = request.GET.get('orden')
    otros = request.GET.getlist('otros[]')
    rest = request.GET.getlist('rest[]')

    active_filters = []

    if is_valid_queryparam(tipo):
        resultados = resultados.filter(tipo__icontains = tipo)
        active_filters.append(ActiveFilter("Propiedad: {}".format(tipo), "tipo"))

    if is_valid_queryparam(oferta):
        resultados = resultados.filter(oferta__icontains = oferta)
        active_filters.append(ActiveFilter("Oferta: En {}".format(oferta), "oferta" ))

    if is_valid_queryparam(precio_min):
        resultados = resultados.filter(precio__gte = precio_min)
        active_filters.append(ActiveFilter("Precio mín: {}".format(precio_min), "precio_min" ))

    if is_valid_queryparam(precio_max):
        resultados = resultados.filter(precio__lte = precio_max)
        active_filters.append(ActiveFilter("Precio max: {}".format(precio_max), "precio_max" ))

    if is_valid_queryparam(estado):
            resultados = resultados.filter(estado__icontains = estado)
            active_filters.append(ActiveFilter("En: {}".format(estado), "estado" ))


    if is_valid_queryparam(habitaciones):
        resultados = resultados.filter(habitaciones = habitaciones)
        active_filters.append(ActiveFilter("Con: {} habitaciones".format(habitaciones), "habitaciones" ))


    if is_valid_queryparam(metros_terreno):
        limites = metros_terreno.split("-")
        if limites[0] == '':
            resultados = resultados.filter(metros_terreno__lte = limites[1])
            active_filters.append(ActiveFilter("Máximo {}m2 de terreno".format(limites[1]), "metros_terreno" ))

        elif limites[1] == '':
            resultados = resultados.filter(metros_terreno__gte = limites[0])
            active_filters.append(ActiveFilter("Mínimo {}m2 de terreno".format(limites[0]), "metros_terreno" ))
        else:
            resultados = resultados.filter(metros_terreno__gte = limites[0])
            resultados = resultados.filter(metros_terreno__lte = limites[1])
            active_filters.append(ActiveFilter("Mínimo {}m2, Máximo {}m2 de terreno".format(limites[0], limites[1]), "metros_terreno" ))

    if is_valid_queryparam(metros_construccion):
        limites = metros_construccion.split("-")
        if limites[0] == '':
            resultados = resultados.filter(metros_construccion__lte = limites[1])
            active_filters.append(ActiveFilter("Máximo {}m2 de construcción".format(limites[1]), "metros_construccion" ))

        elif limites[1] == '':
            resultados = resultados.filter(metros_construccion__gte = limites[0])
            active_filters.append(ActiveFilter("Mínimo {}m2 de construcción".format(limites[0]), "metros_construccion" ))

        else:
            resultados = resultados.filter(metros_construccion__gte = limites[0])
            resultados = resultados.filter(metros_construccion__lte = limites[1])
            active_filters.append(ActiveFilter("Mínimo {}m2, Máximo {}m2 de construcción".format(limites[0], limites[1]), "metros_construccion" ))

    if is_valid_queryparam(banos):
        if banos == "4-":
            resultados = resultados.filter(banos__gte = 4)
            active_filters.append(ActiveFilter("más de 4 baños", "banos" ))
        else:
            resultados = resultados.filter(banos = banos)
            active_filters.append(ActiveFilter("{} baños".format(banos), "banos" ))

    if is_valid_queryparam(pisos):
        if pisos == "3-":
            resultados = resultados.filter(pisos__gte = 3)
            active_filters.append(ActiveFilter("más de 3 pisos", "pisos" ))
        else:
            resultados = resultados.filter(pisos = pisos)
            active_filters.append(ActiveFilter("{} pisos".format(pisos), "pisos" ))

    if is_valid_queryparam(garage):
        if garage == "0":
            resultados = resultados.filter(Q(garaje=None) | Q(garaje=0))
            active_filters.append(ActiveFilter("sin estacionamiento", "garage" ))
        elif garage == "3-":
            resultados = resultados.filter(garaje__gte = 3)
            active_filters.append(ActiveFilter("más de 3 lugares de estacionamiento", "garage" ))
        else:
            resultados = resultados.filter(garaje = garage)
            active_filters.append(ActiveFilter("{} lugares de estacionamiento".format(garage), "garage" ))

    if is_valid_queryparam(orden):
        if orden == "precio":
            resultados = resultados.order_by("-precio")
            active_filters.append(ActiveFilter("Orden por precio", "orden" ))

    if len(otros)>0:
        resultados = resultados.filter(otros__contains=otros)
        for o in otros:
            active_filters.append(ActiveFilter("Otros: " + o, "otros[]", o ))

    if len(rest)>0:
        resultados = resultados.filter(restricciones__contains=rest)
        for r in rest:
            active_filters.append(ActiveFilter("Restricciones: " + r, "rest[]", r ))




    locale.setlocale( locale.LC_ALL, '' )
    for r in resultados:
        r.precio = locale.currency(r.precio, grouping=True)
        r.precio = r.precio[0:-3]

    return render(request, 'propiedades/properties.html',{'resultados': resultados, 'active_filters': active_filters})



@login_required
def myPropertiesView(request):
    if 'visualizar_mis_propiedades' in request.session['permissions']:
        locale.setlocale( locale.LC_ALL, '' )
        user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
        list = Propiedad.objects.filter(propietario = user_logged, estado_visible = True)
        for l in list:
            l.precio = locale.currency(l.precio, grouping=True)
            l.precio = l.precio[0:-3]
            if l.fecha_corte:
                l.fecha_modificacion = (l.fecha_corte - datetime.date.today()).days

        images = Temp.objects.filter(propietario = user_logged)
        for img in images:
            img.imagen = None
            img.save()
        images.delete()

        no_pub = Propiedad.objects.filter(propietario = user_logged, estado_visible = True, estado_activo = False, estado_revision = False).count()

        return render(request, 'propiedades/myProperties.html', {'list': list, 'no_pub': no_pub})
    else:
        raise Http404



"""
#vista de propiedades en revisión
checa si tiene permiso de revision (admins, revisores)
solo filtra las que tengan estatus revision
manda el usuario logeado para la funcionalidad de agregarse/quitarse como revisor
NOTA: por ahora, solo el usuario logeado puede agregarse/quitarse a si mismo como revisor
"""
@login_required
def enRevisionView(request):
    if 'visualizar_peticiones' in request.session['permissions']:
        locale.setlocale( locale.LC_ALL, '' )
        user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado

        if user_logged.rol.nombre is 'Revisor':
            list = Propiedad.objects.filter(estado_revision = True, revisor__isnull=True, estado_visible = True)
        else:
            list = Propiedad.objects.filter(estado_revision = True, estado_visible = True)

        for l in list:
            l.precio = locale.currency(l.precio, grouping=True)
            l.precio = l.precio[0:-3]
        return render(request, 'propiedades/enRevision.html', {'list': list, 'user':user_logged})
    else:
        raise Http404


@login_required
def newPropertyView(request):
    if 'registrar_propiedad' in request.session['permissions']:
        form = CrearPropiedadForma()
        user_logged = TachyonUsuario.objects.get(user = request.user)
        images = Temp.objects.filter(propietario = user_logged)
        for img in images:
            img.imagen = None
            img.save()
        images.delete()
        return render(request, 'propiedades/newProperty.html', {'form': form})
    else:
        raise Http404

def codigosView(request):
    if request.method == 'POST':
        data = []
        codigo = CodigoPostal.objects.filter(codigo = request.POST.get('codigo'))
        if(codigo.count() > 0):
            data.append(serializers.serialize('json', codigo, cls=LazyEncoder))
            return JsonResponse({"info": data})
        else:
            response = JsonResponse({"error": "No existe ese código postal"})
            response.status_code = 500
            # Regresamos la respuesta de error interno del servidor
            return response

    else:
        response = JsonResponse({"error": "No se mandó por el método correcto"})
        response.status_code = 500
        # Regresamos la respuesta de error interno del servidor
        return response

# Aplicar marca de agua a fotos de un folder
def add_watermark(path):
    # Si no hay objeto de la marca de agua, no hace nada
    if MARCA_AGUA.objects.count() == 0:
        print("no hay logo para la marca de agua")
        return
    else: 
        # Atrapar cualquier error, ya sea archivo no compatible, dimensiones, accesos, etc
        try:
            # Dimensiones auxiliares, m = fracción de la imagen a usar, margen = margen lateral
            # ej m = 6, el logo ocupa 1/6. margen = 10, 10 pixeles desde el borde al logo
            m = 6
            margen = 10
            wm = MARCA_AGUA.objects.first().imagen # Recuperar el obj
            for filename in os.listdir(path):
                image = Image.open(path + '/' + filename)
                imageWidth, imageHeight = image.width, image.height
                watermark = Image.open(wm)
                # dividir la imagen entre m y actualizarla
                logoW, logoH = int(imageWidth/m), int(imageHeight/m)
                watermark.thumbnail( (logoW, logoH) )
                # el thumbnail no divide exactamente, recuperar nuevas dimensiones
                newW, newH = watermark.width, watermark.height
                # Usar la esquina inf der
                placeToPaste = (imageWidth - newW - margen, imageHeight - newH - margen)
                image.paste(watermark, placeToPaste, watermark)
                image.save(path + '/' + filename)
                print("WM Saved at " + path + '/' + filename)
                image.close()
                if filename == os.listdir(path)[-1]:
                    watermark.close()
        except Exception as e:
            print("no se pudo aplicar marca de agua")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)


@login_required
def createPropertyView(request):
    if 'registrar_propiedad' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
            form = CrearPropiedadForma(request.POST, request.FILES)
            # files = request.FILES.getlist('extra')
            # print(form.errors)
            if form.is_valid():
                # Sacar los datos del la forma
                oferta = form.cleaned_data['oferta']
                tipo = form.cleaned_data['tipo']
                titulo = form.cleaned_data['titulo']
                desc = form.cleaned_data['desc']
                habs = form.cleaned_data['habs']
                banos = form.cleaned_data['banos']
                garaje = form.cleaned_data['garaje']
                pais = form.cleaned_data['pais']
                estado = form.cleaned_data['estado']
                codigo_postal = form.cleaned_data['codigo_postal']
                colonia = form.cleaned_data['colonia']
                direccion = form.cleaned_data['direccion']
                precio = form.cleaned_data['precio']
                negociable = form.cleaned_data['negociable']
                dif = form.cleaned_data['dif']
                m_terr = form.cleaned_data['m_terr']
                m_cons = form.cleaned_data['m_cons']
                pisos = form.cleaned_data['pisos']
                portada = form.cleaned_data['portada']
                # extra = form.cleaned_data['extra']
                video = form.cleaned_data['video']
                otros = request.POST.getlist('otros[]')
                rest = request.POST.getlist('rest[]')

                if estado == "Queretaro" or estado == "querétaro" or estado == "queretaro":
                    estado = "Querétaro"

                files = Temp.objects.filter(propietario = user_logged)

                if files.filter(activo = True).count() < 5 or files.filter(activo = True).count() > 20:
                    # Eliminar las imagenes temporales
                    for f in files:
                        f.imagen = None
                        f.save()
                    files.delete()
                    request.session['notification_session_msg'] = "La cantidad de imágenes es incorrecta, por favor inténtelo de nuevo."
                    request.session['notification_session_type'] = "Danger"
                    return redirect('/propiedades/myProperties/')

                # Crear el objeto de Propiedad
                propiedad = Propiedad()
                propiedad.propietario = user_logged
                propiedad.titulo = titulo
                propiedad.tipo = tipo
                propiedad.oferta = oferta
                propiedad.descripcion = desc
                if(habs != None):
                    propiedad.habitaciones = habs
                if(banos != None):
                    propiedad.banos = banos
                if(garaje != None):
                    propiedad.garaje = garaje
                if(pisos != None):
                    propiedad.pisos = pisos
                propiedad.metros_terreno = m_terr
                propiedad.metros_construccion = m_cons
                propiedad.pais = pais
                propiedad.codigo_postal = codigo_postal
                propiedad.estado = estado
                propiedad.colonia = colonia
                propiedad.direccion = direccion
                propiedad.precio = precio
                propiedad.negociable = negociable
                if(dif != None):
                    propiedad.diferenciador = dif
                if(video != None):
                    propiedad.video = video
                if len(otros) > 0:
                    propiedad.otros = otros
                if len(rest) > 0:
                    propiedad.restricciones = rest

                # Guardar propiedad para poder guardar las imagenes
                propiedad.save()

                # Guardar imagen de portada
                propiedad.portada = portada
                propiedad.save()

                # Guardar imagenes de la propiedad
                i = 1
                for f in files.filter(activo = True):
                    fotos = Foto()
                    fotos.propiedad = propiedad
                    fotos.orden = i
                    fotos.save()
                    img = f.imagen
                    fotos.imagen = File(img, os.path.basename(img.name))
                    fotos.save()
                    img.close()
                    i = i + 1
                # Add marca agua
                #image_folder = "{}\\user_{}\\property_{}\\".format(settings.MEDIA_ROOT, propiedad.propietario.pk, propiedad.pk)
                #image_folder_extra = image_folder + "extra\\"
                #image_folder_main = image_folder + "main\\"
                image_folder = "{}/user_{}/property_{}/".format(settings.MEDIA_ROOT, propiedad.propietario.pk, propiedad.pk)
                image_folder_extra = image_folder + "extra/"
                image_folder_main = image_folder + "main/"

                add_watermark(image_folder_extra)
                add_watermark(image_folder_main)

                # Eliminar las imagenes temporales
                for f in files:
                    f.imagen = None
                    f.save()
                files.delete()

                request.session['notification_session_msg'] = "Se ha añadido la propiedad exitosamente."
                request.session['notification_session_type'] = "Success"
                return redirect('/propiedades/myProperties/')

            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404

def validatePropertyView(request, id):
    if 'solicitar_revision' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
            propiedad = Propiedad.objects.filter(pk = id).first()
            if propiedad:
                propiedad.estado_revision = True
                propiedad.save()
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


def deletePropertyView(request, id):
    print(request.session['permissions'])
    if 'eliminar_propiedad' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
            propiedad = Propiedad.objects.filter(pk = id).first()
            if propiedad:
                if propiedad.propietario == user_logged:    # Evitar que los usuarios puedan borrar propiedades ajenas

                    propiedad.estado_visible = False
                    propiedad.estado_activo = False
                    propiedad.estado_revision = False
                    propiedad.fecha_corte = None
                    propiedad.portada = None
                    propiedad.save()

                    images = Foto.objects.filter(propiedad = id)
                    for img in images:
                        img.imagen = None
                        img.save()
                    images.delete()

                    return HttpResponse('OK')
                else:
                    response = JsonResponse({"error": "No puedes borrar propiedades ajenas"})
                    response.status_code = 401
                    return response
            else:
                response = JsonResponse({"error": "No existe ese usuario"})
                response.status_code = 402
                return response
        else:
            response = JsonResponse({"error": "No se mandó por el método correcto"})
            response.status_code = 500
            # Regresamos la respuesta de error interno del servidor
            return response
    else:   # Si el rol del usuario no es Propietario, Admin, o Super Admin, no puede borrar
        response = JsonResponse({"error": "No tienes los permisos necesarios"})
        response.status_code = 404
        return response


@login_required
def addRevisorView(request):
    if 'seleccionar_peticion' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
            id_prop = request.POST.get('id_prop') #checa el id de la propiedad del request

            #No se mandó nada por el POST
            if id_prop is None:
                response = JsonResponse({"error": "Error en el servidor, vuelva a intentarlo más tarde"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            propiedad = Propiedad.objects.filter(pk = id_prop).first()

            #La propiedad no existe
            if propiedad is None:
                response = JsonResponse({"error": "No existe esta propiedad"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            #La propiedad no está en estado de revisión
            if not propiedad.estado_revision:
                response = JsonResponse({"error": "La propiedad no está en revisión"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            #La propiedad ya tiene revisor
            if propiedad.revisor is not None:
                response = JsonResponse({"error": "La propiedad ya tiene revisor asignado"})
                response.status_code = 400
                # Regresamos la respuesta de error
                return response

            propiedad.revisor = user_logged
            propiedad.save()
            return HttpResponse('OK')

        #No se hizo método POST
        else:
            response = JsonResponse({"error": "No se mandó por el método correcto"})
            response.status_code = 500
            # Regresamos la respuesta de error interno del servidor
            return response
    else: # Si el rol del usuario no es revisor no puede entrar a la página
        raise Http404


@login_required
def removeRevisorView(request):
    if 'seleccionar_peticion' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
            id_prop = request.POST.get('id_prop') #checa el id de la propiedad del request

            #No se mandó nada por el POST
            if id_prop is None:
                response = JsonResponse({"error": "Error en el servidor, vuelva a intentarlo más tarde"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            propiedad = Propiedad.objects.filter(pk = id_prop).first()

            #La propiedad no existe
            if propiedad is None:
                response = JsonResponse({"error": "No existe esta propiedad"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            #La propiedad no está en estado de revisión
            if not propiedad.estado_revision:
                response = JsonResponse({"error": "La propiedad no está en revisión"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            #La propiedad no tiene revisor
            if propiedad.revisor is None:
                response = JsonResponse({"error": "La propiedad no tiene revisor asignado"})
                response.status_code = 400
                # Regresamos la respuesta de error
                return response

            propiedad.revisor = None
            propiedad.save()
            return HttpResponse('OK')

        #No se hizo método POST
        else:
            response = JsonResponse({"error": "No se mandó por el método correcto"})
            response.status_code = 500
            # Regresamos la respuesta de error interno del servidor
            return response

    else: # Si el rol del usuario no es revisor no puede entrar a la página
        raise Http404


@login_required
def misRevisionesView(request):
    if 'seleccionar_peticion' in request.session['permissions']:
        locale.setlocale( locale.LC_ALL, '' )
        user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
        list = Propiedad.objects.filter(revisor = user_logged, estado_visible = True)
        for l in list:
            l.precio = locale.currency(l.precio, grouping=True)
            l.precio = l.precio[0:-3]
        return render(request, 'propiedades/misRevisiones.html', {'list': list, 'user':user_logged})
    else: # Si el rol del usuario no es revisor no puede entrar a la página
        raise Http404


@login_required
def validateAsRevisorView(request):
    if 'aceptar_rechazar_peticion' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
            id_prop = request.POST.get('id_prop') #checa el id de la propiedad del request

            #No se mandó nada por el POST
            if id_prop is None:
                response = JsonResponse({"error": "Error en el servidor, intente acualizar la página e inténtelo de nuevo (e-id00)"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            propiedad = Propiedad.objects.filter(pk = id_prop).first()

            #La propiedad no existe
            if propiedad is None:
                response = JsonResponse({"error": "No existe esta propiedad"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            #La propiedad no está en estado de revisión
            if not propiedad.estado_revision:
                response = JsonResponse({"error": "La propiedad no está en revisión"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            #La propiedad no tiene revisor
            if propiedad.revisor is None:
                response = JsonResponse({"error": "La propiedad no tiene revisor asignado"})
                response.status_code = 400
                # Regresamos la respuesta de error
                return response

            if propiedad.estado_activo is True:
                response = JsonResponse({"error": "La propiedad ya ha sido validada (err-inconsistencia)"})
                response.status_code = 400
                # Regresamos la respuesta de error
                return response

            valores=['aceptada', 'rechazada']
            #no se envió valor de aceptada o rechazada, no tiene comentarios
            if request.POST.get('aor') not in valores:
                response = JsonResponse({"error": "Error en la solicitud, vuelva a intentarlo más tarde (err-decis-null)"})
                response.status_code = 400
                # Regresamos la respuesta de error
                return response

            #no se envió valor de aceptada o rechazada, no tiene comentarios
            if request.POST.get('coms') is '':
                response = JsonResponse({"error": "Error en la solicitud, vuelva a intentarlo más tarde (err-coms-null)"})
                response.status_code = 400
                # Regresamos la respuesta de error
                return response

            coms = propiedad.comentarios = request.POST.get('coms')

            rvw = propiedad.revisor

            user = propiedad.propietario.user

            #La propiedad fue aceptada
            if request.POST.get('aor') == "aceptada":
                print("aceptada")
                propiedad.estado_revision = False
                propiedad.estado_activo = True
                propiedad.fecha_publicacion = datetime.date.today()
                propiedad.fecha_corte = add_months(datetime.date.today(), 3)
                propiedad.revisor = None
                propiedad.save()
                if (user.email != 'test@test.com'):
                    # Enviar correo con codigo de registro
                    message = Mail(
                        from_email='no-reply@conexioninmueble.com',
                        to_emails=user.email,
                        subject='Conexión Inmueble - '+ propiedad.titulo +': Publicada',
                        plain_text_content='''Saludos '''+ propiedad.propietario.nombre +''',
                        \n\nEstamos felices de informarle que su propiedad ha sido aceptada por nuestros revisores. Su propiedad ya fue publicada y podrá ser accedida por los usuarios de la página.
                        \n\nEnlace a su Propiedad: \n\t - https://conexioninmueble.com/propiedades/property/'''+ str(propiedad.pk) +'''
                        \nRecuerde que para editar su propiedad, primero debe darla de baja. Puede dar de baja su propiedad desde la página cuando lo necesite.
                        \n\nMuchas gracias por elegirnos para promocionar su propiedad, le deseamos mucha suerte en la '''+ propiedad.oferta +''' de la misma.
                        \n\nPOR FAVOR NO RESPONDA A ESTE CORREO'''
                        )
                    try:
                        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                        response = sg.send(message)
                        print(response.status_code)
                        print(response.body)
                        print(response.headers)
                    except Exception as e:
                        print(e)
                request.session['notification_session_msg'] = "Se ha aceptado la propiedad exitosamente."
                request.session['notification_session_type'] = "Success"
            elif request.POST.get('aor') == "rechazada":
                print("rechazada")
                propiedad.estado_revision = False
                propiedad.estado_activo = False
                propiedad.save()
                if (user.email != 'test@test.com'):
                    # Enviar correo con codigo de registro
                    message = Mail(
                        from_email='no-reply@conexioninmueble.com',
                        to_emails=user.email,
                        subject='Conexión Inmueble - '+ propiedad.titulo +': Rechazada',
                        plain_text_content='''Saludos '''+ propiedad.propietario.nombre +''',
                        \n\nLamentamos informarle que su propiedad ha sido rechazada por nuestros revisores, por favor lea los siguientes comentarios de nuestros revisores, realice las correcciones necesarias, y vuelva a mandar a revisión su propiedad.
                        \n\nComentarios del Revisor: \n'''+ coms +'''
                        \n\nPara cualquier otra duda sobre su propiedad, envíe un correo electrónico al revisor encargado.
                        \n\nCorreo de Contacto del Revisor:\n\t- '''+rvw.user.email+'''
                        \n\nFAVOR DE CONTACTAR AL REVISOR POR EL CORREO PROPORCIONADO, NO RESPONDER A ESTE CORREO'''
                        )
                    try:
                        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                        response = sg.send(message)
                        print(response.status_code)
                        print(response.body)
                        print(response.headers)
                    except Exception as e:
                        print(e)
                request.session['notification_session_msg'] = "Se ha rechazado la propiedad exitosamente."
                request.session['notification_session_type'] = "Success"

            pc = PropiedadComentario()
            pc.propiedad = propiedad
            pc.comentario = coms
            pc.revisor = rvw
            pc.save()

            return HttpResponse('OK')

        #No se hizo método POST
        else:
            response = JsonResponse({"error": "No se mandó por el método correcto"})
            response.status_code = 500
            # Regresamos la respuesta de error interno del servidor
            return response

    else: # Si el rol del usuario no es revisor no puede entrar a la página
        raise Http404



@login_required
def propertyCommentHistoryView(request):

    if 'aceptar_rechazar_peticion' in request.session['permissions']:
        if request.method == 'GET':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
            id = request.GET.get('id') #checa el id de la propiedad del request

            #No se mandó nada por el GET
            if id is None:
                response = JsonResponse({"error": "Error en el servidor, intente acualizar la página e inténtelo de nuevo (e-id00)"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response

            propiedad = Propiedad.objects.filter(pk = id).first()

            #La propiedad no existe
            if propiedad is None:
                response = JsonResponse({"error": "No existe esta propiedad"})
                response.status_code = 400
                # Regresamos la respuesta de error interno del servidor
                return response


            pcs = PropiedadComentario.objects.filter(propiedad__pk = id)
            data = []
            for p in pcs:
                r = p.revisor
                f = p.fecha
                d = {
                    "revisor": r.nombre+" "+r.apellido_paterno+" "+r.apellido_materno,
                    "fecha": str(f.hour)+":"+str(f.minute)+" "+str(f.day)+"/"+str(f.month)+"/"+str(f.year),
                    "comentario": p.comentario
                }
                data.append(d)
            #data = serializers.serialize('json', data)
            return JsonResponse({"info": data})


        #No se hizo método GET
        else:
            response = JsonResponse({"error": "No se mandó por el método correcto"})
            response.status_code = 500
            # Regresamos la respuesta de error interno del servidor
            return response

    else: # Si el rol del usuario no es revisor no puede entrar a la página
        raise Http404



# Vista para editar una propiedad
@login_required
def editPropertyView(request, id):
    if 'editar_propiedad' in request.session['permissions']:
        form = EditarPropiedadForma()
        propiedad = Propiedad.objects.filter(pk = id).first()
        if propiedad:
            user_logged = TachyonUsuario.objects.get(user = request.user)

            images = Temp.objects.filter(propietario = user_logged)
            for img in images:
                img.imagen = None
                img.save()
            images.delete()

            images = Foto.objects.filter(propiedad = propiedad)

            return render(request, 'propiedades/editProperty.html', {'property': propiedad, 'form': form, 'files': images})
        else:
            raise Http404
    else:
        raise Http404

@login_required
def modifyPropertyView(request, id):
    if 'editar_propiedad' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
            form = EditarPropiedadForma(request.POST, request.FILES)
            # files = request.FILES.getlist('extra')
            # print(form.errors)
            if form.is_valid():
                # Sacar los datos del la forma
                oferta = form.cleaned_data['oferta']
                tipo = form.cleaned_data['tipo']
                titulo = form.cleaned_data['titulo']
                desc = form.cleaned_data['desc']
                habs = form.cleaned_data['habs']
                banos = form.cleaned_data['banos']
                garaje = form.cleaned_data['garaje']
                pais = form.cleaned_data['pais']
                estado = form.cleaned_data['estado']
                codigo_postal = form.cleaned_data['codigo_postal']
                colonia = form.cleaned_data['colonia']
                direccion = form.cleaned_data['direccion']
                precio = form.cleaned_data['precio']
                negociable = form.cleaned_data['negociable']
                dif = form.cleaned_data['dif']
                m_terr = form.cleaned_data['m_terr']
                m_cons = form.cleaned_data['m_cons']
                pisos = form.cleaned_data['pisos']
                portada = form.cleaned_data['portada']
                extra = form.cleaned_data['extra']
                video = form.cleaned_data['video']
                otros = request.POST.getlist('otros[]')
                rest = request.POST.getlist('rest[]')

                files = Temp.objects.filter(propietario = user_logged)

                if files.filter(activo = True).count() < 5 or files.filter(activo = True).count() > 20:
                    # Eliminar las imagenes temporales
                    for f in files:
                        f.imagen = None
                        f.save()
                    files.delete()
                    request.session['notification_session_msg'] = "La cantidad de imágenes es incorrecta, por favor inténtelo de nuevo."
                    request.session['notification_session_type'] = "Danger"
                    return redirect('/propiedades/myProperties/')

                # Crear el objeto de Propiedad
                propiedad = Propiedad.objects.filter(pk = id).first()
                if propiedad:
                    propiedad.titulo = titulo
                    propiedad.tipo = tipo
                    propiedad.oferta = oferta
                    propiedad.descripcion = desc
                    propiedad.habitaciones = habs
                    if banos:
                        propiedad.banos = banos
                    else:
                        propiedad.banos = None
                    propiedad.garaje = garaje
                    propiedad.pisos = pisos
                    propiedad.metros_terreno = m_terr
                    propiedad.metros_construccion = m_cons
                    propiedad.pais = pais
                    propiedad.codigo_postal = codigo_postal
                    propiedad.estado = estado
                    propiedad.colonia = colonia
                    propiedad.direccion = direccion
                    propiedad.precio = precio
                    propiedad.negociable = negociable
                    if(dif != None):
                        propiedad.diferenciador = dif
                    if(video != None):
                        propiedad.video = video
                    propiedad.estado_revision = False
                    propiedad.estado_activo = False
                    propiedad.otros = otros
                    propiedad.restricciones = rest
                    propiedad.fecha_corte = None

                    # Guardar propiedad para poder guardar las imagenes
                    propiedad.save()

                    nuevaPortada = False
                    nuevasImagenes = False

                    # Guardar imagen de portada nueva si se añadio una
                    if portada:
                        propiedad.portada = portada
                        propiedad.save()

                    # Guardar imagenes de la propiedad nuevas si se añadieron
                    images = Foto.objects.filter(propiedad = id)
                    for img in images:
                        img.imagen = None
                        img.save()
                    images.delete()

                    # Guardar imagenes de la propiedad
                    i = 1
                    for f in files.filter(activo = True):
                        fotos = Foto()
                        fotos.propiedad = propiedad
                        fotos.orden = i
                        fotos.save()
                        img = f.imagen
                        fotos.imagen = File(img, os.path.basename(img.name))
                        fotos.save()
                        img.close()
                        i = i + 1

                    # Eliminar las imagenes temporales
                    for f in files:
                        f.imagen = None
                        f.save()
                    files.delete()


                    image_folder = "{}/user_{}/property_{}/".format(settings.MEDIA_ROOT, propiedad.propietario.pk, propiedad.pk)
                    image_folder_extra = image_folder + "extra/"
                    image_folder_main = image_folder + "main/"
                    
                    add_watermark(image_folder_extra)
                    add_watermark(image_folder_main)


                    request.session['notification_session_msg'] = "Se ha modificado la propiedad exitosamente."
                    request.session['notification_session_type'] = "Success"
                else:
                    request.session['notification_session_msg'] = "Ha ocurrido un error, inténtelo de nuevo más tarde."
                    request.session['notification_session_type'] = "Danger"
                return redirect('/propiedades/myProperties/')

            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404


def search(request):
    return null


@login_required
def modifyPropertyReviewerView(request, id):
    if 'editar_propiedad_revision' in request.session['permissions']:
        if request.method == 'POST':
            propiedad = Propiedad.objects.filter(pk = id).first()
            if propiedad:
                n_titulo = request.POST.get('titulo')
                n_difer = request.POST.get('difer')
                n_desc = request.POST.get('desc')
                if propiedad.titulo != n_titulo:
                    propiedad.titulo = n_titulo
                if propiedad.diferenciador != n_difer:
                    propiedad.diferenciador = n_difer
                if propiedad.descripcion != n_desc:
                    propiedad.descripcion = n_desc
                propiedad.save()
                request.session['notification_session_msg'] = "Se ha modificado la propiedad exitosamente."
                request.session['notification_session_type'] = "Success"
            else:
                request.session['notification_session_msg'] = "Ha ocurrido un error, inténtelo de nuevo más tarde."
                request.session['notification_session_type'] = "Danger"
            return redirect('/propiedades/mis-revisiones/')
        else:
            raise Http404
    else:
        raise Http404


def contactOwnerView(request, id):
    if request.method == 'POST':
        propiedad = Propiedad.objects.filter(pk = id).first()
        if propiedad:
            user = propiedad.propietario.user
            correo = request.POST.get('email')
            #asunto = request.POST.get('asunto')
            msg = request.POST.get('msg')
            print(msg)
            #return redirect('/propiedades/property/'+str(id))
            if (user.email != 'test@test.com'):
                # Enviar correo con codigo de registro
                message = Mail(
                    from_email='no-reply@conexioninmueble.com',
                    to_emails=user.email,
                    subject='Conexión Inmueble - '+ propiedad.titulo,
                    plain_text_content=''+msg+'\n\n\nCorreo de Contacto del Usuario:\n\t- '+correo+'\n\nFAVOR DE CONTACTAR AL USUARIO POR EL CORREO PROPORCIONADO, NO RESPONDER A ESTE CORREO'
                    # html_content='<p>'+msg+'</p><br>\
                    #     <p>Correo de Contacto del Usuario: </p>\
                    #     <ul>\
                    #     <li><strong>'+correo+'</strong></li>\
                    #     </ul>'
                    )
                try:
                    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                    response = sg.send(message)
                    print(response.status_code)
                    print(response.body)
                    print(response.headers)
                except Exception as e:
                    print(e)

            request.session['notification_session_msg'] = "Se ha mandado un correo al propietario."
            request.session['notification_session_type'] = "Success"
            return redirect('/propiedades/property/'+str(id))
        else:
            request.session['notification_session_msg'] = "Ha ocurrido un error, inténtelo de nuevo más tarde."
            request.session['notification_session_type'] = "Danger"
    else:
        raise Http404



def unpublishPropertyView(request):
    if request.method == 'POST':
        user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
        id = request.POST.get('id')
        propiedad = Propiedad.objects.filter(pk = id).first()
        if propiedad:
            if propiedad.propietario == user_logged:    # Evitar que los usuarios puedan editar propiedades ajenas
                propiedad.estado_activo = False
                propiedad.estado_revision = False
                propiedad.fecha_corte = None
                propiedad.save()
                return HttpResponse('OK')
            else:
                response = JsonResponse({"error": "No puedes editar propiedades ajenas"})
                response.status_code = 401
                return response
        else:
            response = JsonResponse({"error": "No existe esta propiedad"})
            response.status_code = 402
            return response
    else:
        response = JsonResponse({"error": "La solicitud no se mandó por el método correcto"})
        response.status_code = 500
        # Regresamos la respuesta de error interno del servidor
        return response


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)


@login_required
def uploadImagesView(request):
    if 'registrar_propiedad' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado

            file = request.FILES.get('images')
            i = request.POST.get('i')

            # print(file.name)
            # print(i)
            # files = [request.FILES.get('images[%d]' % i)
            #     for i in range(0, len(request.FILES))]

            # Guardar imagenes de la propiedad
            temp = Temp()
            temp.propietario = user_logged
            temp.orden = i
            temp.save()
            temp.imagen = file
            temp.save()

            return HttpResponse('OK')

        else:
            raise Http404
    else:
        raise Http404


@login_required
def deleteImagesView(request):
    if 'registrar_propiedad' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado

            i = request.POST.get('id')

            # print(i)

            # Desactivar imagenes de la propiedad
            t = Temp.objects.filter(orden = i).first()

            if t:
                t.activo = False
                t.save()
                return JsonResponse({"info": "Éxito"})
            else:
                response = JsonResponse({"error": "No existe esa imagen"})
                response.status_code = 401
                return response
        else:
            raise Http404
    else:
        raise Http404


# Vista de las Propiedades de usuario/agencia
def userView(request, id):

    resultados = Propiedad.objects.filter(estado_activo = True)
    user = id
    agencia = True

    if id.isnumeric():
        resultados = resultados.filter(propietario__pk = id)
        user = TachyonUsuario.objects.filter(pk = id, estado_eliminado = False, estado_registro = True).first()
        if not user:
            raise Http404
        agencia = False
    else:
        resultados = resultados.filter(propietario__nombre_agencia__icontains = id)
        if resultados.count() <= 0:
            raise Http404

    locale.setlocale( locale.LC_ALL, '' )
    for r in resultados:
        r.precio = locale.currency(r.precio, grouping=True)
        r.precio = r.precio[0:-3]

    return render(request, 'propiedades/propertiesUser.html',{'resultados': resultados, 'user': user, 'agencia': agencia})
