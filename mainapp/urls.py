from django.urls import path
from .views import *

urlpatterns = [

   path('delegate-record/<pk>/<app_name>/<model_name>/<url>/', delegate_record, name="delegate_record"),     
   path('un-authorized-return/<app_name>/<model_name>/<url>/', unauthorized_return, name="unauthorized_return"),
   path('get_data/', get_data, name='get_data'),
]

