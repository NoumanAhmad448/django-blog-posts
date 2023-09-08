from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone
from api_v1.models.create_post_model import CreatePostModel

class BookmarkPostModel(models.Model):
    #  neither change the order of POST_CHOICES nor the first tuple

    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    ID = "id"
    USER = "user"
    POST = "post"

    post = models.ForeignKey(CreatePostModel,on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _('Bookmark Post')
        verbose_name_plural = _('Bookmark Posts')
        db_table = 'bookmark_posts'
