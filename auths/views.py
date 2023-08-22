from django.shortcuts import render,redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .forms.registeration_form import RegisterationForm
from .forms.login_form import LoginForm
from django.contrib.auth.models import User
from .keywords.html_page import HtmlPage as Words
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms.update_pass import UpdatePassForm
from django.utils import translation as tran
from django.conf import settings
from .models import PasswordHistory

@api_view(["GET","POST"])
@permission_classes((permissions.AllowAny,))
def register_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("/", permanent=True)
        return render(request, Words.reg_url)

    elif request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            # duplicate email validation
            if User.objects.filter(email=form.cleaned_data["email"]).exists():
                form.add_error("email",tran.gettext("Duplicate email has found"))
                return render(request, Words.reg_url, {"form": form})

            user = User.objects.create_user(form.cleaned_data["email"], form.cleaned_data["email"], form.cleaned_data["password"])
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()

            return redirect("/login",permanent=True)
        else:
            return render(request, Words.reg_url, {"form": form})


def current_posts(request):
    context = {"test": "test2"}
    return render(request, "auths/index.html", context)


@api_view(["GET","POST"])
@permission_classes((permissions.AllowAny,))
def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect("/", permanent=True)
        return render(request, Words.login_url)
    elif request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(request, username=form.cleaned_data["email"], password=form.cleaned_data["password"])
                if user is not None:
                    login(request, user)
                    return redirect("/",permanent=True)
                else:
                   form.add_error("email", tran.gettext("Either email or password is wrong"))
                   return render(request, Words.login_url, {"form": form})
            else:
                return render(request, Words.login_url, {"form": form})

@login_required
def logout_user(request):
    logout(request)
    return redirect("/")


@login_required
def forgot_password(request):
    if request.method == 'GET':
        user = request.user
        password_history = PasswordHistory.objects.filter(user_id=user.id).order_by("-created_at")[:1]
        return render(request, Words.update_pass_url, {"password_history": password_history[0]})

    elif request.method == 'POST':
        form = UpdatePassForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["password"]
            c_password = form.cleaned_data["c_password"]
            if new_password == c_password:
                user = request.user
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    PasswordHistory.objects.create(user_id=user.id)
                    return redirect("/",permanent=True)
                else:
                    return render(request, Words.update_pass_url, {"form": form})
            else:
                form.add_error("password", tran.gettext("Both passwords are not same"))
                return render(request, Words.update_pass_url, {"form": form})
        else:
            return render(request, Words.update_pass_url, {"form": form})
