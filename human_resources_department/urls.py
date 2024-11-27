from django.urls import path,include
from .views import *

urlpatterns = [
    

    path('leavemanagement-create/', leavemanagement_create, name="leavemanagement_create"),
    path('leavemanagement-list/', leavemanagement_list, name="leavemanagement_list"),
    path('leavemanagement-pa/<pk>/', leavemanagement_pa, name="leavemanagement_pa"),
    path('leavemanagement-update/<str:code>/', leavemanagement_update, name="leavemanagement_update"),
    path('leavemanagement-view/<str:code>/', leavemanagement_view, name="leavemanagement_view"),
    path('leavemanagement-delete/<pk>/', leavemanagement_delete, name="leavemanagement_delete"),
    path('leavemanagement-authorize-request/<pk>/', leavemanagement_authorize_request, name="leavemanagement_authorize_request"),
    path('staffproductivity-create/', staffproductivity_create, name="staffproductivity_create"),
    path('staffproductivity-list/', staffproductivity_list, name="staffproductivity_list"),
    path('staffproductivity-pa/<pk>/', staffproductivity_pa, name="staffproductivity_pa"),
    path('staffproductivity-update/<str:code>/', staffproductivity_update, name="staffproductivity_update"),
    path('staffproductivity-view/<str:code>/', staffproductivity_view, name="staffproductivity_view"),
    path('staffproductivity-delete/<pk>/', staffproductivity_delete, name="staffproductivity_delete"),
    path('staffproductivity-authorize-request/<pk>/', staffproductivity_authorize_request, name="staffproductivity_authorize_request"),
    path('trainingdevelopment-create/', trainingdevelopment_create, name="trainingdevelopment_create"),
    path('trainingdevelopment-list/', trainingdevelopment_list, name="trainingdevelopment_list"),
    path('trainingdevelopment-pa/<pk>/', trainingdevelopment_pa, name="trainingdevelopment_pa"),
    path('trainingdevelopment-update/<str:code>/', trainingdevelopment_update, name="trainingdevelopment_update"),
    path('trainingdevelopment-view/<str:code>/', trainingdevelopment_view, name="trainingdevelopment_view"),
    path('trainingdevelopment-delete/<pk>/', trainingdevelopment_delete, name="trainingdevelopment_delete"),
    path('trainingdevelopment-authorize-request/<pk>/', trainingdevelopment_authorize_request, name="trainingdevelopment_authorize_request"),
    path('staffturnover-create/', staffturnover_create, name="staffturnover_create"),
    path('staffturnover-list/', staffturnover_list, name="staffturnover_list"),
    path('staffturnover-pa/<pk>/', staffturnover_pa, name="staffturnover_pa"),
    path('staffturnover-update/<str:code>/', staffturnover_update, name="staffturnover_update"),
    path('staffturnover-view/<str:code>/', staffturnover_view, name="staffturnover_view"),
    path('staffturnover-delete/<pk>/', staffturnover_delete, name="staffturnover_delete"),
    path('staffturnover-authorize-request/<pk>/', staffturnover_authorize_request, name="staffturnover_authorize_request"),
]