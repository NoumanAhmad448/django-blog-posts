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


@login_required(login_url="/login")
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
    return render(request,Words.index_url, {"post" : post})
