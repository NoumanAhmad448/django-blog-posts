from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone

class CreatePostModel(models.Model):
    #  neither change the order of POST_CHOICES nor the first tuple
    POST_CHOICES = [
        ("api", _("API")),
        ("web", _("web")),
    ]
    source = models.CharField(choices=POST_CHOICES,verbose_name=_("Post Source"), max_length=100)
    title = models.CharField(verbose_name=_("Post Title"),max_length=500)
    tags = models.CharField(verbose_name=_("Post Tags"),max_length=500)
    descrip = models.CharField(max_length=10000)
    should_display = models.BooleanField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = _('User Post')
        verbose_name_plural = _('User Posts')
        db_table = 'create_posts'
