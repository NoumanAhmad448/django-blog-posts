from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.current_posts, name="latest_posts"),
    path("register", views.register_user, name="register_user"),
]