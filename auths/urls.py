from django.urls import path,include
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.current_posts, name="latest_posts"),
    path("register", views.register_user, name="register_user"),
    path("login", views.login_user, name="login_user"),
    path("logout", views.logout_user, name="logout"),
    path("update-password", views.forgot_password, name="update_password"),
]