"""
URL configuration for accounts_report_v13_frontend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp.api import RegisterServiceplan
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include

urlpatterns = [
    path('financial_department/', include('financial_department.urls')),
    path('administration_department/', include('administration_department.urls')),
    path('aging_reports/', include('aging_reports.urls')),
    path('human_resources_department/', include('human_resources_department.urls')),
    path('itand_misdepartment/', include('itand_misdepartment.urls')),
    path('operations_department/', include('operations_department.urls')),
    path('riskand_compliance_department/', include('riskand_compliance_department.urls')),
    path('marketingand_customer_relations_department/', include('marketingand_customer_relations_department.urls')),
    path('', include('user_management.urls')),
    path('mainapp', include('mainapp.urls')),
    path('mainapp', include('workflow.urls')),
    path('register-serviceplan/', RegisterServiceplan.as_view(), name='register-serviceplan' ),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
