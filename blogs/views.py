from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from .keywords.html_page import HtmlPage as Words
from api_v1.models import CreatePostModel
from django.shortcuts import get_object_or_404

@api_view(["GET","POST"])
def create_post(request):
    if request.method == 'GET':
        return Response()

    elif request.method == 'POST':
        # serializer = SnippetSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pass
@permission_classes((permissions.AllowAny,))
def current_post(request, post_id):
    post = get_object_or_404(CreatePostModel,id=post_id)
    return render(request,Words.index_url, {"post" : post})
