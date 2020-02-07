from django.shortcuts import render
from django.http import JsonResponse

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
