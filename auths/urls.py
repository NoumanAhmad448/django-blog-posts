from django.urls import path
from . import views
from django.contrib.flatpages import views as flat_view

urlpatterns = [
    path('', views.current_posts, name="latest_posts"),
    path("register", views.register_user, name="register_user"),
    path("login", views.login_user, name="login_user"),
    path("logout", views.logout_user, name="logout"),
    path("update-password", views.forgot_password, name="update_password"),
    path("test-cel", views.test_cel, name="test_cel"),
    path("about-us/", flat_view.flatpage, {"url": "/about/"}, name="about"),
    path("license/", flat_view.flatpage, {"url": "/license/"}, name="license"),
]