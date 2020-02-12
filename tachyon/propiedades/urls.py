from django.urls import path

from . import views

urlpatterns = [
    path('property', views.propertyView, name='porperty'),
    path('properties', views.propertiesView, name='porperties'),
]
