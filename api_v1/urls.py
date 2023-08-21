from django.contrib import admin
from django.urls import include, path
from .serializer import UserViewSet
from rest_framework import routers
from django.urls import re_path
from . import views

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path("", include(router.urls), name="users"),
    path("user/<int:user_id>", views.user, name="user_info"),
    path("generate_token", views.create_token, name="create_token"),
]