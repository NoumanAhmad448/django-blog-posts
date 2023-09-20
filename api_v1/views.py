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
from .models.create_post_model import CreatePostModel
from django.shortcuts import get_object_or_404
from .serializers.create_post_serializer import PostSerializer
from django.utils import timezone
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
            user = User.objects.filter(email=email).first()
            user_serializer = CustomUserSerializer(user)
            if user_serializer.data is not None:
                response["is_success"] = True
                response["data"] = user_serializer.data

                token = Token.objects.filter(user_id=user_serializer.data["id"]).first()
                if token is not None:
                    response["token"] = token.__str__()
                else:
                    token = Token.objects.create(user=current_user)
                    response["token"] = token.__str__()

                return JsonResponse(response, status=http_status.HTTP_200_OK)
            else:
                response["message"] = "seriizer did not return antyhing"
                return JsonResponse(response, status=http_status.HTTP_400_BAD_REQUEST)
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
    post_model = CreatePostModel()
    api_resp = ApiResponse()
    api_resp.is_success = False
    api_resp.data = {}
    if settings.DEBUG:
        api_resp.debug["HTTP_AUTHORIZATION"] = request.META["HTTP_AUTHORIZATION"] if "HTTP_AUTHORIZATION" in request.META else _("no such header is found")
        api_resp.debug["CONTENT_TYPE"] = request.META["CONTENT_TYPE"] if "CONTENT_TYPE" in request.META else _("no such header is found")

    if is_user_not_authenticated(request):
        status = http_status.HTTP_400_BAD_REQUEST
        api_resp.message = _("user is not authorized")
        return JsonResponse(api_resp.send_response(), status=status, safe=False)

    if request.META["CONTENT_TYPE"] == "application/json":
        data = JSONParser().parse(request)
    else:
        data = request.POST
        data._mutable = True

    create_post_form = CreatePostForm(data)
    status = http_status.HTTP_400_BAD_REQUEST

    if(create_post_form.is_valid()):
        api_resp.data = data
        api_resp.is_success = True
        status = http_status.HTTP_200_OK
        user = request.user

        id = data[post_model.ID] if post_model.ID in data else None
        if id and id is not None:
            create_post = CreatePostModel.objects.filter(id=id,user=user).first()
        else:
            create_post = CreatePostModel()
        if create_post:
            create_post.user=user
            create_post.source=create_post_form.cleaned_data[post_model.SOURCE]
            create_post.title=create_post_form.cleaned_data[post_model.TITLE]
            create_post.tags=create_post_form.cleaned_data[post_model.TAGS]
            create_post.descrip=create_post_form.cleaned_data[post_model.DESCRIP]

            if user.is_superuser or user.is_staff:
                create_post.should_display = 1
            else:
                create_post.should_display = 0
            if id is not None:
                create_post.updated_at = timezone.now()

            create_post.save()

            if id and id is None:
                api_resp.data[post_model.ID] = id
            else:
                api_resp.data[post_model.ID] = create_post.id
        else:
            status = http_status.HTTP_403_FORBIDDEN
            api_resp.is_success = False
            api_resp.message = _("this user is not authorized to update the post")
    else:
        api_resp.data = data
        if data["source"] and data["source"] == CreatePostModel.POST_CHOICES[0][0]:
            api_resp.message = create_post_form.errors.as_json()
        else:
            api_resp.message = create_post_form.errors.as_ul()
    return JsonResponse(api_resp.send_response(), status=status, safe=False)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication,TokenAuthentication])
def get_post(request):
    api_resp = ApiResponse()
    api_resp.is_success = False
    api_resp.data = {}

    if settings.DEBUG:
        api_resp.debug["HTTP_AUTHORIZATION"] = request.META["HTTP_AUTHORIZATION"] if "HTTP_AUTHORIZATION" in request.META else _("no such header is found")
        api_resp.debug["CONTENT_TYPE"] = request.META["CONTENT_TYPE"] if "CONTENT_TYPE" in request.META else _("no such header is found")

    if is_user_not_authenticated(request):
        status = http_status.HTTP_400_BAD_REQUEST
        api_resp.message = _("user is not authorized")
        return JsonResponse(api_resp.send_response(), status=status, safe=False)

    request = JSONParser().parse(request)
    from .forms.get_post import GetPostForm
    form = GetPostForm(request)
    if form.is_valid():
        api_resp.is_success = True
        post = get_object_or_404(CreatePostModel.objects.filter(id=form.cleaned_data[form.POST_ID]))
        api_resp.data = PostSerializer(post).data
        status = http_status.HTTP_200_OK
        api_resp.message=_("post has been found")
    else:
        api_resp.message =  form.errors.as_json()
        status=http_status.HTTP_400_BAD_REQUEST
    return JsonResponse(api_resp.send_response(), status=status, safe=False)

@api_view(['GET'])
def posts(request):
    api_resp = ApiResponse()
    api_resp.is_success = False
    api_resp.data = {}

    posts = CreatePostModel.objects.filter(should_display=1)
    status= http_status.HTTP_200_OK
    if posts.exists():
        api_resp.is_success = True
        api_resp.data = PostSerializer(posts,many=True).data
    else:
        api_resp.message = "no post is found"
    return JsonResponse(api_resp.send_response(), status=status, safe=False)