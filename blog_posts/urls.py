from django.contrib import admin
from django.urls import include, path
from django.urls import re_path


urlpatterns = [
    path("", include('auths.urls')),
    path('api/', include("api_v1.urls")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]