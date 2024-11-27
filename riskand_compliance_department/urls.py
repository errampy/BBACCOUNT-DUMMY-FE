from django.urls import path,include
from .views import *

urlpatterns = [
    

    path('compliance-create/', compliance_create, name="compliance_create"),
    path('compliance-list/', compliance_list, name="compliance_list"),
    path('compliance-pa/<pk>/', compliance_pa, name="compliance_pa"),
    path('compliance-update/<str:code>/', compliance_update, name="compliance_update"),
    path('compliance-view/<str:code>/', compliance_view, name="compliance_view"),
    path('compliance-delete/<pk>/', compliance_delete, name="compliance_delete"),
    path('compliance-authorize-request/<pk>/', compliance_authorize_request, name="compliance_authorize_request"),
    path('fraudmonitoring-create/', fraudmonitoring_create, name="fraudmonitoring_create"),
    path('fraudmonitoring-list/', fraudmonitoring_list, name="fraudmonitoring_list"),
    path('fraudmonitoring-pa/<pk>/', fraudmonitoring_pa, name="fraudmonitoring_pa"),
    path('fraudmonitoring-update/<str:code>/', fraudmonitoring_update, name="fraudmonitoring_update"),
    path('fraudmonitoring-view/<str:code>/', fraudmonitoring_view, name="fraudmonitoring_view"),
    path('fraudmonitoring-delete/<pk>/', fraudmonitoring_delete, name="fraudmonitoring_delete"),
    path('fraudmonitoring-authorize-request/<pk>/', fraudmonitoring_authorize_request, name="fraudmonitoring_authorize_request"),
    path('riskassessment-create/', riskassessment_create, name="riskassessment_create"),
    path('riskassessment-list/', riskassessment_list, name="riskassessment_list"),
    path('riskassessment-pa/<pk>/', riskassessment_pa, name="riskassessment_pa"),
    path('riskassessment-update/<str:code>/', riskassessment_update, name="riskassessment_update"),
    path('riskassessment-view/<str:code>/', riskassessment_view, name="riskassessment_view"),
    path('riskassessment-delete/<pk>/', riskassessment_delete, name="riskassessment_delete"),
    path('riskassessment-authorize-request/<pk>/', riskassessment_authorize_request, name="riskassessment_authorize_request"),
]