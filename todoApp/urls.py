"""todoApp URL Configuration

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
from django.urls import path, include,re_path

from rest_framework import routers
from django.conf.urls import url  # Importação necessária
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
  

  
# schema_view = get_schema_view(
#    openapi.Info(
#       title="Dummy API",
#       default_version='v1',
#       description="Dummy description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@dummy.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
   ),
   public=True,
#    permission_classes=(permissions.AllowAny,),
)
# router = routers.DefaultRouter()



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', admin.site.urls),
    path('users/',include('users.urls')),
    path('tarefa/', include('tarefa.urls')),
    path("api/v1/",
         include([
             path('users/',include('users.urls')),
    path('tarefa/', include('tarefa.urls')),
                # path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
                path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
         ]))
    #
    #  url('playground/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # url('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
# urlpatterns = format_suffix_patterns(urlpatterns)
