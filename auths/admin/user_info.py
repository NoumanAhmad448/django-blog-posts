from django.contrib import admin
from ..models import UserInfo
from django.utils.translation import gettext_lazy as _

@admin.register(UserInfo)
class UserInfo(admin.ModelAdmin):
    list_filter = ["ip_address"]