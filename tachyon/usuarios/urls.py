from django.urls import path
from django.contrib.auth import views as auth_views


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
    path('<int:user_id>', views.profile, name='profile'),
    path('<int:user_id>/edit', views.edit_user, name='edit_user'),
    path('deleteUser/<int:id>', views.deleteUserView, name='deleteUser'),
    path('adminCreateUser', views.adminCreateUserView, name='adminCreateUser'),
    path('adminVerifyCreateUser', views.adminVerifyCreateUser, name="adminVerifyCreateUser"),
    path('reset_password', auth_views.PasswordResetView.as_view(template_name = 'usuarios/reset_password_mail.html', email_template_name='usuarios/password_reset_email.html', subject_template_name='usuarios/password_reset_subject.txt'), name='reset_password'),
    path('reset_password_done', auth_views.PasswordResetDoneView.as_view(template_name = 'usuarios/reset_password_sent.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'usuarios/reset_password_change.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'usuarios/reset_password_success.html'), name='password_reset_complete'),
    path('changeRol', views.changeRolView, name='changeRol'),
    path('editPassword', views.editPasswordView, name='editPassword'),
    path('changePassword', views.changePasswordView, name='changePassword'),
]
