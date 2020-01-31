from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('confirm', views.confirm, name='confirm'),

]
