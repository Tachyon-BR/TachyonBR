from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('confirm/<int:id>', views.confirm, name='confirm'),
    path('createUser', views.createUser, name='createUser'),
    path('verificar_correo', views.verificar_correo, name='verificar_correo'),
    path('confirmMail', views.confirmMail, name='confirmMail'),
]
