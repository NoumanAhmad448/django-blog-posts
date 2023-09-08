from django.contrib import admin
from ..models import CreatePostModel
from django.utils.translation import gettext_lazy as _
from api_v1.models.create_post_model import CreatePostModel
from blogs.models.post_bookmark_model import BookmarkPostModel

@admin.register(CreatePostModel)
class CreatePostAdmin(admin.ModelAdmin):
    bookmark_post = CreatePostModel()
    list_filter = [bookmark_post.ID,bookmark_post.CREATED_AT]
    fieldsets = [
        (
            _("POST ID"),
            {
                "fields": [bookmark_post.TITLE,bookmark_post.DESCRIP],
            },
        ),
        (
            _("Advanced options"),
            {
                "classes": ["collapse"],
                "fields": [bookmark_post.CREATED_AT,bookmark_post.UPDATED_AT,bookmark_post.SHOULD_DISPLAY],
            },
        ),
    ]

@admin.register(BookmarkPostModel)
class BookmarkPostsAdmin(admin.ModelAdmin):
    bookmark_post = BookmarkPostModel()
    list_filter = [bookmark_post.ID,bookmark_post.CREATED_AT]
    fieldsets = [
        (
            _("POST ID"),
            {
                "fields": [bookmark_post.USER,bookmark_post.POST],
            },
        ),
        (
            _("Advanced options"),
            {
                "classes": ["collapse"],
                "fields": [bookmark_post.CREATED_AT,bookmark_post.UPDATED_AT],
            },
        ),
    ]
