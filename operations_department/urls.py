from django.urls import path,include
from .views import *

urlpatterns = [
    

    path('loandisbursement-create/', loandisbursement_create, name="loandisbursement_create"),
    path('loandisbursement-list/', loandisbursement_list, name="loandisbursement_list"),
    path('loandisbursement-pa/<pk>/', loandisbursement_pa, name="loandisbursement_pa"),
    path('loandisbursement-update/<str:code>/', loandisbursement_update, name="loandisbursement_update"),
    path('loandisbursement-view/<str:code>/', loandisbursement_view, name="loandisbursement_view"),
    path('loandisbursement-delete/<pk>/', loandisbursement_delete, name="loandisbursement_delete"),
    path('loandisbursement-authorize-request/<pk>/', loandisbursement_authorize_request, name="loandisbursement_authorize_request"),
    path('portfolioquality-create/', portfolioquality_create, name="portfolioquality_create"),
    path('portfolioquality-list/', portfolioquality_list, name="portfolioquality_list"),
    path('portfolioquality-pa/<pk>/', portfolioquality_pa, name="portfolioquality_pa"),
    path('portfolioquality-update/<str:code>/', portfolioquality_update, name="portfolioquality_update"),
    path('portfolioquality-view/<str:code>/', portfolioquality_view, name="portfolioquality_view"),
    path('portfolioquality-delete/<pk>/', portfolioquality_delete, name="portfolioquality_delete"),
    path('portfolioquality-authorize-request/<pk>/', portfolioquality_authorize_request, name="portfolioquality_authorize_request"),
    path('clientoutreach-create/', clientoutreach_create, name="clientoutreach_create"),
    path('clientoutreach-list/', clientoutreach_list, name="clientoutreach_list"),
    path('clientoutreach-pa/<pk>/', clientoutreach_pa, name="clientoutreach_pa"),
    path('clientoutreach-update/<str:code>/', clientoutreach_update, name="clientoutreach_update"),
    path('clientoutreach-view/<str:code>/', clientoutreach_view, name="clientoutreach_view"),
    path('clientoutreach-delete/<pk>/', clientoutreach_delete, name="clientoutreach_delete"),
    path('clientoutreach-authorize-request/<pk>/', clientoutreach_authorize_request, name="clientoutreach_authorize_request"),
    path('branchperformance-create/', branchperformance_create, name="branchperformance_create"),
    path('branchperformance-list/', branchperformance_list, name="branchperformance_list"),
    path('branchperformance-pa/<pk>/', branchperformance_pa, name="branchperformance_pa"),
    path('branchperformance-update/<str:code>/', branchperformance_update, name="branchperformance_update"),
    path('branchperformance-view/<str:code>/', branchperformance_view, name="branchperformance_view"),
    path('branchperformance-delete/<pk>/', branchperformance_delete, name="branchperformance_delete"),
    path('branchperformance-authorize-request/<pk>/', branchperformance_authorize_request, name="branchperformance_authorize_request"),
]