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

# Create your views here.

#Esta clase sirve para serializar los objetos de los modelos.
class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Cotizacion):
            return str(obj)
        return super().default(obj)

# Vista de una Propiedad
def propertyView(request):
    return render(request, 'propiedades/property.html')

# Vista de las Propiedades
def indexView(request):
    return render(request, 'propiedades/properties.html')

@login_required
def myPropertiesView(request):
    if 'visualizar_mis_propiedades' in request.session['permissions']:
        return render(request, 'propiedades/myProperties.html')
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


                request.session['notification_session_msg'] = "Se ha añadido la propiedad exitosamente."
                request.session['notification_session_type'] = "Success"
                return render(request, 'propiedades/myProperties.html')

            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404
