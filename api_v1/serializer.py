from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active','id','username', 'email', 'is_staff']
