from django.urls import path

from . import views

urlpatterns = [
    path('property/<int:id>', views.propertyView, name='porperty'),
    path('', views.indexView, name='index'),
    path('myProperties/', views.myPropertiesView, name='myProperties'),
    path('newProperty/', views.newPropertyView, name='newProperty'),
    path('codigos/', views.codigosView, name='codigos'),
    path('createProperty/', views.createPropertyView, name='createProperty'),
    path('validateProperty/<int:id>', views.validatePropertyView, name='validateProperty'),
    path('enRevision/', views.enRevisionView, name='enRevision'),
    path('addRevisor/',views.addRevisorView, name="addRevisor"),
    path('removeRevisor/',views.removeRevisorView, name="removeRevisor"),
    path('editProperty/<int:id>',views.editPropertyView, name="editProperty"),
    path('modifyProperty/<int:id>',views.modifyPropertyView, name="modifyProperty"),
]
