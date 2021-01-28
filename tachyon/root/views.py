from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from propiedades.models import *
import json
import random
import locale

# Create your views here.
def indexView(request):
    return render(request, 'root/base.html')


def notificationSession(request):         # Funcion que se llama con un ajax para dar retroalimentacion al usuario al crear staff
    if ('notification_session_msg' in request.session) and ('notification_session_type' in request.session):
        msg = request.session['notification_session_msg']
        del request.session['notification_session_msg']
        type = request.session['notification_session_type']
        del request.session['notification_session_type']
        return JsonResponse({
                            "msg": msg,
                            "type": type
                            })
    else:
        return JsonResponse({
                            "msg": 'No existe variable de sesión notification_session_msg',
                            "type": 'No existe variable de sesión notification_session_type'
                            })

def randomProperty(request):
    locale.setlocale( locale.LC_ALL, '' )
    last = Propiedad.objects.filter(estado_activo = True).count()

    if last == 0:
        return JsonResponse({"error": True})

    index = random.randint(0, last-1)

    p = Propiedad.objects.filter(estado_activo = True)[index]
    p.precio = locale.currency(p.precio, grouping=True)
    p.precio = p.precio[0:-3]

    data = []

    data.append(serializers.serialize("json", [p], ensure_ascii = False))

    return JsonResponse({"error": False, "data": data})
