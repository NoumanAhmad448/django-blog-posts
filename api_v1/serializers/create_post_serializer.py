from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone

class PostSerializer(serializers.Serializer):
    #  neither change the order of POST_CHOICES nor the first tuple
    POST_CHOICES = [
        ("api", _("API")),
        ("web", _("web")),
    ]
    id = serializers.IntegerField(read_only=True)
    source = serializers.ChoiceField(choices=POST_CHOICES)
    title = serializers.CharField(max_length=500)
    tags = serializers.CharField(max_length=500)
    descrip = serializers.CharField(max_length=10000)
    should_display = serializers.BooleanField()
    user = serializers.ReadOnlyField(source="user.id")
    created_at = serializers.DateTimeField(default=timezone.now)
    updated_at = serializers.DateTimeField()