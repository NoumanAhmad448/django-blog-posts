from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

class PasswordHistory(models.Model):
    user_id = models.IntegerField(verbose_name=_("User Key"))
    created_at = models.DateTimeField(default=timezone.now,verbose_name=_("Requested Date"))

    @property
    @admin.display(
        description="combo",
    )
    def id_date(self):
        return f"{self.user_id} - {self.created_at}"

    class Meta:
        verbose_name = _('User Password History')
        verbose_name_plural = _('User Password Histories')

