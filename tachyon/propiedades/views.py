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

# Create your views here.

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
