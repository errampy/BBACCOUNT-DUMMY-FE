from django.urls import path,include
from .views import *

urlpatterns = [
    

    path('loanlossprovision-create/', loanlossprovision_create, name="loanlossprovision_create"),
    path('loanlossprovision-list/', loanlossprovision_list, name="loanlossprovision_list"),
    path('loanlossprovision-pa/<pk>/', loanlossprovision_pa, name="loanlossprovision_pa"),
    path('loanlossprovision-update/<str:code>/', loanlossprovision_update, name="loanlossprovision_update"),
    path('loanlossprovision-view/<str:code>/', loanlossprovision_view, name="loanlossprovision_view"),
    path('loanlossprovision-delete/<pk>/', loanlossprovision_delete, name="loanlossprovision_delete"),
    path('loanlossprovision-authorize-request/<pk>/', loanlossprovision_authorize_request, name="loanlossprovision_authorize_request"),
    path('balancesheet-create/', balancesheet_create, name="balancesheet_create"),
    path('balancesheet-list/', balancesheet_list, name="balancesheet_list"),
    path('balancesheet-pa/<pk>/', balancesheet_pa, name="balancesheet_pa"),
    path('balancesheet-update/<str:code>/', balancesheet_update, name="balancesheet_update"),
    path('balancesheet-view/<str:code>/', balancesheet_view, name="balancesheet_view"),
    path('balancesheet-delete/<pk>/', balancesheet_delete, name="balancesheet_delete"),
    path('balancesheet-authorize-request/<pk>/', balancesheet_authorize_request, name="balancesheet_authorize_request"),
    path('incomestatement-create/', incomestatement_create, name="incomestatement_create"),
    path('incomestatement-list/', incomestatement_list, name="incomestatement_list"),
    path('incomestatement-pa/<pk>/', incomestatement_pa, name="incomestatement_pa"),
    path('incomestatement-update/<str:code>/', incomestatement_update, name="incomestatement_update"),
    path('incomestatement-view/<str:code>/', incomestatement_view, name="incomestatement_view"),
    path('incomestatement-delete/<pk>/', incomestatement_delete, name="incomestatement_delete"),
    path('incomestatement-authorize-request/<pk>/', incomestatement_authorize_request, name="incomestatement_authorize_request"),
    path('cashflowstatement-create/', cashflowstatement_create, name="cashflowstatement_create"),
    path('cashflowstatement-list/', cashflowstatement_list, name="cashflowstatement_list"),
    path('cashflowstatement-pa/<pk>/', cashflowstatement_pa, name="cashflowstatement_pa"),
    path('cashflowstatement-update/<str:code>/', cashflowstatement_update, name="cashflowstatement_update"),
    path('cashflowstatement-view/<str:code>/', cashflowstatement_view, name="cashflowstatement_view"),
    path('cashflowstatement-delete/<pk>/', cashflowstatement_delete, name="cashflowstatement_delete"),
    path('cashflowstatement-authorize-request/<pk>/', cashflowstatement_authorize_request, name="cashflowstatement_authorize_request"),
]