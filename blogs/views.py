from django.shortcuts import render
from django.http import HttpResponse
import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

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

