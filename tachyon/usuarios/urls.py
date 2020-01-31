from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('verifyLogin/', views.verifyLogin, name='verifyLogin'),
    path('logout/', views.logoutView, name='logout'),
]
