from django.urls import path

from . import views

urlpatterns = [
    path('property', views.propertyView, name='porperty'),
    path('', views.indexView, name='index'),
    path('myProperties', views.myPropertiesView, name='myProperties'),
]
