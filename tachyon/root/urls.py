from django.urls import path

from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('notificationSession', views.notificationSession, name='notificationSession')
]
