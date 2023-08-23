from django import forms
from django.utils.translation import gettext_lazy as _
from ..models.create_post_model import CreatePostModel


class CreatePostForm(forms.Form):
    source = forms.ChoiceField(error_messages={"required": _("source is required")},choices=CreatePostModel.POST_CHOICES)
    title = forms.CharField(error_messages={"required": _("post title is required")},max_length=500)
    tags = forms.CharField(error_messages={"required": _("post tags is required")},max_length=500)
    descrip = forms.CharField(error_messages={"required" : _("post description is required"),
            "max_length": _("post description must be under 10,000 characters")},
            max_length=10000)
    should_display = forms.BooleanField(required=False)
