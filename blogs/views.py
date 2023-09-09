from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .keywords.html_page import HtmlPage as Words
from api_v1.models import CreatePostModel
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from api_v1.views import create_post as create_post_api
from api_v1.generic_funs import ApiResponse
from django.shortcuts import redirect
import json
from django.urls import reverse
from .models import BookmarkPostModel
import datetime
from django.views.decorators.cache import cache_page
from dotenv import load_dotenv
import os
load_dotenv()


env = os.environ

REDIS_TIMEOUT= int(60*30 if env.get("REDIS_TIMEOUT") is None else env.get("REDIS_TIMEOUT"))


@login_required(login_url="/login")
@cache_page(REDIS_TIMEOUT)
def create_post(request):
    post_model = CreatePostModel()
    if request.method == 'GET':
        data = {}
        errors = {}
        if "errors" in request.session and request.session["errors"] is not None:
            errors = request.session["errors"]
            del request.session["errors"]
        if request.GET.get("post_id") is not None:
            data = get_object_or_404(CreatePostModel.objects.filter(id=request.GET.get("post_id")).
                                     values(post_model.ID,post_model.TITLE, post_model.DESCRIP,post_model.TAGS))
        return render(request,Words.create_post_url, {"data": data, "errors": errors})

    elif request.method == 'POST':
        response = create_post_api(request)
        response = json.loads(response.content)
        api_response = ApiResponse()
        if response[api_response.IS_SUCCESS]:
            if False:
                return redirect(reverse("current_post", args=(response[api_response.DATA]["post_id"],)))
            else:
                return redirect(reverse("create-post")+"?post_id="+str(response[api_response.DATA]["id"]).strip(),
                                {"data" : response[api_response.DATA]})
        else:
            if "id" in response[api_response.DATA] and response[api_response.DATA]["id"] is not None:
                request.session["errors"] = response[api_response.MESSAGE]
                return  redirect(reverse("create-post")+"?post_id="+str(response[api_response.DATA]["id"]).strip())
            else:
                return render(request, Words.create_post_url, {"errors": response[api_response.MESSAGE]})



@permission_classes((permissions.AllowAny,))
def current_post(request, post_id):
    post = get_object_or_404(CreatePostModel,id=post_id)
    user = request.user
    is_post_bookmarked = False
    if user is not None:
        is_post_bookmarked = BookmarkPostModel.objects.filter(post=post.id,user=user.id).exists()
    return render(request,Words.index_url, {"post" : post,
                                            "is_post_bookmarked": is_post_bookmarked})

@login_required(login_url="/login")
@cache_page(REDIS_TIMEOUT)
def show_posts(request):
    posts = CreatePostModel.objects.filter(user_id=request.user.id).order_by("-created_at")
    return render(request, Words.show_posts_url, {"posts": posts})

@login_required(login_url="/login")
def bookmark_post(request):
    if request.method == 'GET':
        bookmark_posts = BookmarkPostModel.objects.filter(user=request.user.id)
        return render(request, Words.bookmark_posts_url, {"bookmark_posts": bookmark_posts})

    if request.method == 'POST':
        post_id = request.POST["post_id"]
        post = get_object_or_404(CreatePostModel.objects.filter(id=post_id))
        user = request.user
        bookmark_post = BookmarkPostModel.objects.filter(user=user.id,post=post_id)
        is_save = False
        if not bookmark_post.exists():
            bookmark_post = BookmarkPostModel()
            is_save = True

        bookmark_post.user = user
        bookmark_post.post = post
        bookmark_post.updated_at = datetime.datetime.now()
        if is_save:
            bookmark_post.save()
        else:
            bookmark_post.update()
        return redirect(reverse("bookmark_post"))

@login_required(login_url="/login")
def unbookmark_post(request):
    if request.method == 'POST':
        post_id = request.POST["post_id"]
        print(post_id)
        post = get_object_or_404(CreatePostModel.objects.filter(id=post_id))
        BookmarkPostModel.objects.filter(user=request.user.id,post=post.id).delete()
        return redirect(reverse("current_post", kwargs={"post_id":post.id}))
