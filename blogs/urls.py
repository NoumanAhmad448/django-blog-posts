from django.urls import path
from . import views

urlpatterns = [
    path('<int:post_id>', views.current_post, name="current_post"),
    path('create-post', views.create_post, name="create-post"),
    path('show-posts', views.show_posts, name="show_posts"),
    path('bookmark_post', views.bookmark_post, name="bookmark_post"),
    path('unbookmark_post', views.unbookmark_post, name="unbookmark_post"),
]