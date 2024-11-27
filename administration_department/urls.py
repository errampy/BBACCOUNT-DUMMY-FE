from django.urls import path,include
from .views import *

urlpatterns = [
    

    path('officeexpense-create/', officeexpense_create, name="officeexpense_create"),
    path('officeexpense-list/', officeexpense_list, name="officeexpense_list"),
    path('officeexpense-pa/<pk>/', officeexpense_pa, name="officeexpense_pa"),
    path('officeexpense-update/<str:code>/', officeexpense_update, name="officeexpense_update"),
    path('officeexpense-view/<str:code>/', officeexpense_view, name="officeexpense_view"),
    path('officeexpense-delete/<pk>/', officeexpense_delete, name="officeexpense_delete"),
    path('officeexpense-authorize-request/<pk>/', officeexpense_authorize_request, name="officeexpense_authorize_request"),
    path('assetmanagement-create/', assetmanagement_create, name="assetmanagement_create"),
    path('assetmanagement-list/', assetmanagement_list, name="assetmanagement_list"),
    path('assetmanagement-pa/<pk>/', assetmanagement_pa, name="assetmanagement_pa"),
    path('assetmanagement-update/<str:code>/', assetmanagement_update, name="assetmanagement_update"),
    path('assetmanagement-view/<str:code>/', assetmanagement_view, name="assetmanagement_view"),
    path('assetmanagement-delete/<pk>/', assetmanagement_delete, name="assetmanagement_delete"),
    path('assetmanagement-authorize-request/<pk>/', assetmanagement_authorize_request, name="assetmanagement_authorize_request"),
    path('logisticsandfleetmanagement-create/', logisticsandfleetmanagement_create, name="logisticsandfleetmanagement_create"),
    path('logisticsandfleetmanagement-list/', logisticsandfleetmanagement_list, name="logisticsandfleetmanagement_list"),
    path('logisticsandfleetmanagement-pa/<pk>/', logisticsandfleetmanagement_pa, name="logisticsandfleetmanagement_pa"),
    path('logisticsandfleetmanagement-update/<str:code>/', logisticsandfleetmanagement_update, name="logisticsandfleetmanagement_update"),
    path('logisticsandfleetmanagement-view/<str:code>/', logisticsandfleetmanagement_view, name="logisticsandfleetmanagement_view"),
    path('logisticsandfleetmanagement-delete/<pk>/', logisticsandfleetmanagement_delete, name="logisticsandfleetmanagement_delete"),
    path('logisticsandfleetmanagement-authorize-request/<pk>/', logisticsandfleetmanagement_authorize_request, name="logisticsandfleetmanagement_authorize_request"),
]