from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class GetPostForm(forms.Form):
    validate_numbers = RegexValidator(r'^[0-9+]', _('Only digits are allowed'))
    POST_ID = "post_id"
    post_id = forms.CharField(validators=[validate_numbers],
                                error_messages={"required": _("post id is required")},)
