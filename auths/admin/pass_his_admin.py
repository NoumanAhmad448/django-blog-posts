from typing import Any, List, Tuple
from django.contrib import admin
from django.db.models.query import QuerySet
from ..models import PasswordHistory
import datetime
from django.utils.translation import gettext_lazy as _

class PassHisFifDaysFilter(admin.SimpleListFilter):

    title = _("Days Filter")
    parameter_name = "created_at"
    fifteen_days = "15_days"
    twenty_days = "20_days"

    def lookups(self, request: Any, model_admin: Any) -> List[Tuple[Any, str]]:
        return [
            (self.fifteen_days, _("15 days")),
            (self.twenty_days, _("20 days")),
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == self.fifteen_days:
            return queryset.filter(created_at__gte=datetime.date.today()-datetime.timedelta(days=15))

        if self.value() == self.twenty_days:
            return queryset.filter(created_at__gte=datetime.date.today()-datetime.timedelta(days=20))



@admin.register(PasswordHistory)
class PasswordHistoryAdmin(admin.ModelAdmin):
    list_filter = ["user_id", "created_at",PassHisFifDaysFilter]
    list_display = ["id_date"]
    # exclude = ["created_at"]
    fieldsets = [
        (
            _("User ID"),
            {
                "fields": ["user_id"],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["created_at"],
            },
        ),
    ]