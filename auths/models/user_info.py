from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class UserInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    ip_address = models.GenericIPAddressField(null=True,verbose_name=_("Ip Address"))


    class Meta:
        verbose_name = _('User info')
        verbose_name_plural = _('User info')
        db_table = 'user_info'


