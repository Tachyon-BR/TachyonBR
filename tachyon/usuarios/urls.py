from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create, name='create'),
    path('login/', views.loginView, name='login'),
    path('verifyLogin/', views.verifyLogin, name='verifyLogin'),
    path('logout/', views.logoutView, name='logout'),
    path('confirm/<int:id>', views.confirm, name='confirm'),
    path('createUser', views.createUser, name='createUser'),
    path('verificar_correo', views.verificar_correo, name='verificar_correo'),
    path('confirmMail', views.confirmMail, name='confirmMail'),
    path('', views.indexView, name='index'),
    path('deleteUser/<int:id>', views.deleteUserView, name='deleteUser'),
    path('adminCreateUserView', views.adminCreateUserView, name='adminCreateUserView'),
    path('adminVerifyCreateUser', views.adminVerifyCreateUser, name="adminVerifyCreateUser")
]
