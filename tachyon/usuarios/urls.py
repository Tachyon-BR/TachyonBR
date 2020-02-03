from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('confirm', views.confirm, name='confirm'),
    path('createUser', views.createUser, name='createUser'),
    path('verificar_correo', views.verificar_correo, name='verificar_correo'),
]
