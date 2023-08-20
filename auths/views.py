
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

@api_view(["GET","POST"])
@permission_classes((permissions.AllowAny,))
def register_user(request):
    if request.method == 'GET':
        return render(request, "auths/register.html")

    elif request.method == 'POST':
        pass


def current_posts(request):
    context = {"test": "test2"}
    return render(request, "auths/index.html", context)