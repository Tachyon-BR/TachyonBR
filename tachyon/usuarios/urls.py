from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('confirm', views.confirm, name='confirm'),
    path('login/', views.loginView, name='login'),
    path('verifyLogin/', views.verifyLogin, name='verifyLogin'),
    path('logout/', views.logoutView, name='logout'),
]
