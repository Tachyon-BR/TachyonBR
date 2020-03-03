from django.urls import path

from . import views

urlpatterns = [
    path('property/', views.propertyView, name='porperty'),
    path('', views.indexView, name='index'),
    path('myProperties/', views.myPropertiesView, name='myProperties'),
    path('newProperty/', views.newPropertyView, name='newProperty'),
    path('codigos/', views.codigosView, name='codigos'),
    path('createProperty/', views.createPropertyView, name='createProperty'),
]
