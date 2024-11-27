from django.urls import path,include
from .views import *

urlpatterns = [
    

    path('loanaging-create/', loanaging_create, name="loanaging_create"),
    path('loanaging-list/', loanaging_list, name="loanaging_list"),
    path('loanaging-pa/<pk>/', loanaging_pa, name="loanaging_pa"),
    path('loanaging-update/<str:code>/', loanaging_update, name="loanaging_update"),
    path('loanaging-view/<str:code>/', loanaging_view, name="loanaging_view"),
    path('loanaging-delete/<pk>/', loanaging_delete, name="loanaging_delete"),
    path('loanaging-authorize-request/<pk>/', loanaging_authorize_request, name="loanaging_authorize_request"),
    path('accountsreceivableaging-create/', accountsreceivableaging_create, name="accountsreceivableaging_create"),
    path('accountsreceivableaging-list/', accountsreceivableaging_list, name="accountsreceivableaging_list"),
    path('accountsreceivableaging-pa/<pk>/', accountsreceivableaging_pa, name="accountsreceivableaging_pa"),
    path('accountsreceivableaging-update/<str:code>/', accountsreceivableaging_update, name="accountsreceivableaging_update"),
    path('accountsreceivableaging-view/<str:code>/', accountsreceivableaging_view, name="accountsreceivableaging_view"),
    path('accountsreceivableaging-delete/<pk>/', accountsreceivableaging_delete, name="accountsreceivableaging_delete"),
    path('accountsreceivableaging-authorize-request/<pk>/', accountsreceivableaging_authorize_request, name="accountsreceivableaging_authorize_request"),
]