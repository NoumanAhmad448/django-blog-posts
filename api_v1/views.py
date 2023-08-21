from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .serializer import CustomUserSerializer
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate

response = {"is_success": False, "data": []}
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def user(request,user_id):
    user_id = user_id
    user = User.objects.filter(id=user_id)
    if user is not None and user.exists():
        user_serializer = CustomUserSerializer(user, many=True)
        response["is_success"]=True
        response["data"] = user_serializer.data[0]
        response["message"] = "user has found"
        return JsonResponse(response, safe=False)
    else:
        response["message"]="user is not found"
        return JsonResponse(response, safe=False)

@api_view(['POST'])
def create_token(request):
    from rest_framework.authtoken.models import Token

    data = JSONParser().parse(request)
    email = data["email"] if "email" in data else None
    password = data["password"] if "password" in data else None
    if email is not None:
        current_user = authenticate(username=email, password=password)

        if current_user is not None:
            user = User.objects.filter(email=email)
            user_serializer = CustomUserSerializer(user, many=True)

            response["is_success"] = True
            response["data"] = user_serializer.data[0]

            token = Token.objects.filter(user_id=user_serializer.data[0]["id"]).first()
            if token is not None:
                response["token"] = token.__str__()
            else:
                token = Token.objects.create(user=current_user)
                response["token"] = token.__str__()

            return JsonResponse(response, status=200)
        else:
            response["message"] = "User credentials are wrong"
            return JsonResponse(response, status=400)
    else:
        response["is_success"] = False
        response["data"] = []
        response["message"] = "email field is required."
        return JsonResponse(response, status=400)