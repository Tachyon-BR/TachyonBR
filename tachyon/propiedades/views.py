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
    user_logged = TachyonUsuario.objects.get(user = request.user) # Obtener el tipo de usuario logeado
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
