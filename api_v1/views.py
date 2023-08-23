from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from .serializer import CustomUserSerializer
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .forms.create_post import CreatePostForm
from rest_framework import status as http_status
from .generic_funs import ApiResponse
from .generic_funs import is_user_not_authenticated
from django.conf import settings

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def user(request,user_id):
    response = {"is_success": False, "data": []}
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

    response = {"is_success": False, "data": []}
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
        response["message"] = _("email field is required")
        return JsonResponse(response, status=400)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
def create_post(request):
    from .models.create_post_model import CreatePostModel
    api_resp = ApiResponse()
    api_resp.is_success = False
    api_resp.data = {}
    if settings.DEBUG:
        api_resp.data["HTTP_AUTHORIZATION"] = request.META["HTTP_AUTHORIZATION"] if "HTTP_AUTHORIZATION" in request.META else _("no such header is found")

    if is_user_not_authenticated(request):
        status = http_status.HTTP_400_BAD_REQUEST
        api_resp.message = _("user is not authorized")
        return JsonResponse(api_resp.send_response(), status=status, safe=False)

    data = JSONParser().parse(request)
    create_post_form = CreatePostForm(data)
    status = http_status.HTTP_400_BAD_REQUEST

    if(create_post_form.is_valid()):
        api_resp.data = data
        api_resp.is_success = True
        status = http_status.HTTP_200_OK
        user = request.user

        create_post = CreatePostModel()
        create_post.user_id=user
        create_post.source=create_post_form.cleaned_data["source"]
        create_post.title=create_post_form.cleaned_data["title"]
        create_post.tags=create_post_form.cleaned_data["tags"]
        create_post.descrip=create_post_form.cleaned_data["descrip"]

        if user.is_superuser or user.is_staff:
            create_post.should_display = 1
        create_post.save()

    else:
        api_resp.data = data
        if data["source"] and data["source"] == CreatePostModel.POST_CHOICES[0][0]:
            api_resp.message = create_post_form.errors.as_json()
        else:
            api_resp.message = create_post_form.errors.as_ul()

    return JsonResponse(api_resp.send_response(), status=status)
