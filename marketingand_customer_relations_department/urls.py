from django.urls import path,include
from .views import *

urlpatterns = [
    

    path('customersatisfaction-create/', customersatisfaction_create, name="customersatisfaction_create"),
    path('customersatisfaction-list/', customersatisfaction_list, name="customersatisfaction_list"),
    path('customersatisfaction-pa/<pk>/', customersatisfaction_pa, name="customersatisfaction_pa"),
    path('customersatisfaction-update/<str:code>/', customersatisfaction_update, name="customersatisfaction_update"),
    path('customersatisfaction-view/<str:code>/', customersatisfaction_view, name="customersatisfaction_view"),
    path('customersatisfaction-delete/<pk>/', customersatisfaction_delete, name="customersatisfaction_delete"),
    path('customersatisfaction-authorize-request/<pk>/', customersatisfaction_authorize_request, name="customersatisfaction_authorize_request"),
    path('clientacquisition-create/', clientacquisition_create, name="clientacquisition_create"),
    path('clientacquisition-list/', clientacquisition_list, name="clientacquisition_list"),
    path('clientacquisition-pa/<pk>/', clientacquisition_pa, name="clientacquisition_pa"),
    path('clientacquisition-update/<str:code>/', clientacquisition_update, name="clientacquisition_update"),
    path('clientacquisition-view/<str:code>/', clientacquisition_view, name="clientacquisition_view"),
    path('clientacquisition-delete/<pk>/', clientacquisition_delete, name="clientacquisition_delete"),
    path('clientacquisition-authorize-request/<pk>/', clientacquisition_authorize_request, name="clientacquisition_authorize_request"),
    path('feedbackandcomplaints-create/', feedbackandcomplaints_create, name="feedbackandcomplaints_create"),
    path('feedbackandcomplaints-list/', feedbackandcomplaints_list, name="feedbackandcomplaints_list"),
    path('feedbackandcomplaints-pa/<pk>/', feedbackandcomplaints_pa, name="feedbackandcomplaints_pa"),
    path('feedbackandcomplaints-update/<str:code>/', feedbackandcomplaints_update, name="feedbackandcomplaints_update"),
    path('feedbackandcomplaints-view/<str:code>/', feedbackandcomplaints_view, name="feedbackandcomplaints_view"),
    path('feedbackandcomplaints-delete/<pk>/', feedbackandcomplaints_delete, name="feedbackandcomplaints_delete"),
    path('feedbackandcomplaints-authorize-request/<pk>/', feedbackandcomplaints_authorize_request, name="feedbackandcomplaints_authorize_request"),
]