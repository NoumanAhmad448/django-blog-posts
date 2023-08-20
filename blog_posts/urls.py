from django.contrib import admin
from django.urls import include, path
from .serializer import UserViewSet
from rest_framework import routers
from django.urls import re_path
from . import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path("", include('auths.urls')),
    re_path('api', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]