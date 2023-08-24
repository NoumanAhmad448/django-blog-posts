from django.urls import path
from . import views

urlpatterns = [
    path('<int:post_id>', views.current_post, name="current_post"),
    path('create-post', views.create_post, name="create-post"),
]