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
    path('deleteProperty/<int:id>', views.deletePropertyView, name='deletePropery'),
    path('unpublishProperty/', views.unpublishPropertyView, name='unpublishProperty'),
    path('enRevision/', views.enRevisionView, name='enRevision'),
    path('addRevisor/',views.addRevisorView, name="addRevisor"),
    path('removeRevisor/',views.removeRevisorView, name="removeRevisor"),
    path('mis-revisiones/',views.misRevisionesView, name="misRevisionesView"),
    path('validateAsRevisor/',views.validateAsRevisorView, name="validateAsRevisor"),
    path('property-comment-history/',views.propertyCommentHistoryView, name="propertyCommentHistory"),
    path('editProperty/<int:id>',views.editPropertyView, name="editProperty"),
    path('modifyProperty/<int:id>',views.modifyPropertyView, name="modifyProperty"),
    path('search/', views.search, name="search"),
    path('modifyPropertyReviewer/<int:id>',views.modifyPropertyReviewerView, name="modifyPropertyReviewer"),
    path('contactOwner/<int:id>',views.contactOwnerView, name="contactOwner"),
    path('uploadImages/',views.uploadImagesView, name="uploadImages"),
    path('deleteImages/',views.deleteImagesView, name="deleteImages"),
]
