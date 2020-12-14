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
        fotos = Foto.objects.filter(propiedad = id)
        link = propiedad.video
        index = link.find('watch?v=')
        if index != -1:
            link = link[0:index] + 'embed/' + link[index + 8:len(link)]
        return render(request, 'propiedades/property.html', {'property': propiedad, 'images': fotos, 'link': link, 'index': index})
    else:
        raise Http404

def is_valid_queryparam(param):
    return param is not None and param != ''

# Vista de las Propiedades
def indexView(request):

    class ActiveFilter():
        def __init__(self, text, attr):
            self.text = text
            self.attr = attr

    resultados = Propiedad.objects.all()
    tipo = request.GET.get('tipo')
    oferta = request.GET.get('oferta')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    estado = request.GET.get('estado')
    habitaciones = request.GET.get('habitaciones')
    metros_terreno = request.GET.get('metros_terreno')
    metros_construccion = request.GET.get('metros_construccion')

    active_filters = []

    if is_valid_queryparam(tipo):
        resultados = resultados.filter(tipo = tipo)
        active_filters.append(ActiveFilter("Propiedad: {}".format(tipo), "tipo"))
    
    if is_valid_queryparam(oferta):
        resultados = resultados.filter(oferta = oferta)
        active_filters.append(ActiveFilter("Oferta: En {}".format(oferta), "oferta" ))
    
    if is_valid_queryparam(precio_min):
        resultados = resultados.filter(precio__gte = precio_min)
        active_filters.append(ActiveFilter("Precio mín: {}".format(precio_min), "precio_min" ))
    
    if is_valid_queryparam(precio_max):
        resultados = resultados.filter(precio__lte = precio_max)
        active_filters.append(ActiveFilter("Precio max: {}".format(precio_max), "precio_max" ))

    if is_valid_queryparam(estado):
            resultados = resultados.filter(estado = estado)
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

    print(active_filters)

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
        return render(request, 'propiedades/myProperties.html', {'list': list})
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
            list = Propiedad.objects.filter(estado_revision = True, revisor__isnull=True)
        else:
            list = Propiedad.objects.filter(estado_revision = True)

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

@login_required
def createPropertyView(request):
    if 'registrar_propiedad' in request.session['permissions']:
        if request.method == 'POST':
            user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
            form = CrearPropiedadForma(request.POST, request.FILES)
            files = request.FILES.getlist('extra')
            print(form.errors)
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

                # Crear el objeto de Propiedad
                propiedad = Propiedad()
                propiedad.propietario = user_logged
                propiedad.titulo = titulo
                propiedad.tipo = tipo
                propiedad.oferta = oferta
                propiedad.descripcion = desc
                if(tipo != 'Terreno'):
                    propiedad.habitaciones = habs
                    propiedad.banos = banos
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

                # Guardar propiedad para poder guardar las imagenes
                propiedad.save()

                # Guardar imagen de portada
                propiedad.portada = portada
                propiedad.save()

                # Guardar imagenes de la propiedad
                i = 1
                for f in files:
                    fotos = Foto()
                    fotos.propiedad = propiedad
                    fotos.orden = i
                    fotos.save()
                    fotos.imagen = f
                    fotos.save()
                    i = i + 1

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
                    propiedad.save()
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
        user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
        list = Propiedad.objects.filter(revisor = user_logged)
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

            #La propiedad fue aceptada
            if request.POST.get('aor') == "aceptada":
                print("aceptada")
                propiedad.estado_revision = True
                propiedad.estado_activo = True
                propiedad.save()
            elif request.POST.get('aor') == "rechazada":
                print("rechazada")
                propiedad.estado_revision = False
                propiedad.estado_activo = False
                propiedad.save()

            pc = PropiedadComentario()
            pc.propiedad = propiedad
            pc.comentario = coms
            pc.revisor = propiedad.revisor
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
            return render(request, 'propiedades/editProperty.html', {'property': propiedad, 'form': form})
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
            files = request.FILES.getlist('extra')
            print(form.errors)
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

                # Crear el objeto de Propiedad
                propiedad = Propiedad.objects.filter(pk = id).first()
                if propiedad:
                    propiedad.titulo = titulo
                    propiedad.tipo = tipo
                    propiedad.oferta = oferta
                    propiedad.descripcion = desc
                    if(tipo != 'Terreno'):
                        propiedad.habitaciones = habs
                        propiedad.banos = banos
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

                    # Guardar propiedad para poder guardar las imagenes
                    propiedad.save()

                    # Guardar imagen de portada nueva si se añadio una
                    if portada:
                        propiedad.portada = portada
                        propiedad.save()

                    # Guardar imagenes de la propiedad nuevas si se añadieron
                    if extra:
                        images = Foto.objects.filter(propiedad = id)
                        for img in images:
                            img.imagen = None
                            img.save()
                        images.delete()
                        i = 1
                        for f in files:
                            fotos = Foto()
                            fotos.propiedad = propiedad
                            fotos.orden = i
                            fotos.save()
                            fotos.imagen = f
                            fotos.save()
                            i = i + 1

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