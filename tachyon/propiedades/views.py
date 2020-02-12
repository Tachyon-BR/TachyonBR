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

# Create your views here.

# Vista de una Propiedad
def propertyView(request):
    return render(request, 'propiedades/property.html')

# Vista de las Propiedades
def propertiesView(request):
    return render(request, 'propiedades/properties.html')
