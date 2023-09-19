from django.urls import path,register_converter,include
from . import views
from .path_converters import NumberConverter
register_converter(NumberConverter, "numeric")

app_name = 'blog'

urlpatterns = [
    path('<numeric:post_id>', views.current_post, name="current_post"),
    # pass the dynamic URLs
    path('blog_posts/',
         include([
             path('create-post', views.create_post, name="create-post"),
             path('show-posts', views.show_posts, name="show_posts"),
            ]
         )),
    path('bookmark_post', views.bookmark_post, name="bookmark_post"),
    path('unbookmark_post', views.unbookmark_post, name="unbookmark_post"),
]