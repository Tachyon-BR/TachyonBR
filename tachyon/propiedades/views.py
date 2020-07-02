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
        return render(request, 'propiedades/property.html', {'property': propiedad})
    else:
        raise Http404

# Vista de las Propiedades
def indexView(request):
    return render(request, 'propiedades/properties.html')

@login_required
def myPropertiesView(request):
    if 'visualizar_mis_propiedades' in request.session['permissions']:
        locale.setlocale( locale.LC_ALL, '' )
        user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el usuario de Tachyon logeado
        list = Propiedad.objects.filter(propietario = user_logged)
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



@login_required
def addRevisorView(request):
    if 'solicitar_revision' in request.session['permissions']:
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