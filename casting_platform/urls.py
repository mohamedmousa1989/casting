"""casting_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from casting_app.views import (
    ApplicationCreate,
    ApplicationList,
    CompanyCreate,
    ProjectCreate,
    RoleCreate,
    TalentCreate,
    TalentRetrieveUpdate,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Casting App API",
        default_version='v1',
        description="Casting platform",
        terms_of_service="https://www.mixfame.com/policies/terms/",
        contact=openapi.Contact(email="contact@mixfame.com    "),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/talent/create/', TalentCreate.as_view(), name='talent_create'),
    path('api/talent/<int:pk>/', TalentRetrieveUpdate.as_view(), name='talent_get_update'),
    path('api/company/create/', CompanyCreate.as_view(), name='company_create'),
    path('api/project/create/', ProjectCreate.as_view(), name='project_create'),
    path('api/role/create/', RoleCreate.as_view(), name='role_create'),
    path('api/role/apply/', ApplicationCreate.as_view(), name='application_create'),
    path('api/role/<int:role_id>/list/', ApplicationList.as_view(), name='application_list'),
]
