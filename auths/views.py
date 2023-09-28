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
from api_v1.models import CreatePostModel
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from django.contrib.sites.shortcuts import get_current_site
from sys import exit
from funs.funs import get_client_ip
from datetime import datetime
import services

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
            # let one person create an account only five times in a day
            ip = get_client_ip(request)
            if services.enable_five_accounts and ip is not None and ip not in settings.LOCAL_IPS:
                ip_count = User.objects.filter(date_joined__date=datetime.now().date(),userinfo__ip_address=ip).count()
                if ip_count>5:
                    form.add_error("email",tran.gettext("You cannot create multiple accounts"))
                    return render(request, Words.reg_url, {"form": form})

            user = User.objects.create_user(form.cleaned_data["email"], form.cleaned_data["email"], form.cleaned_data["password"])
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.save()
            user.userinfo_set.create(ip_address=ip)

            return redirect("/login",permanent=True)
        else:
            return render(request, Words.reg_url, {"form": form})


def current_posts(request):
    posts = CreatePostModel.objects.filter(should_display=1,
                    site__id=get_current_site(request).id).order_by("-created_at")
    paginator = Paginator(posts, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    return render(request, Words.index_url, {"posts": posts})


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
        password_history = PasswordHistory.objects.filter(user_id=user.id).order_by("-created_at")
        password_history = password_history[0] if password_history and password_history.exists() else None
        return render(request, Words.update_pass_url, {"password_history": password_history})

    elif request.method == 'POST':
        form = UpdatePassForm(request.POST)
        form.is_valid()
        if form.is_valid():
            new_password = form.cleaned_data["password"]
            c_password = form.cleaned_data["c_password"]
            if new_password == c_password:
                user = request.user
                if user is not None:
                    user.set_password(new_password)
                    user.save()
                    PasswordHistory.objects.create(user_id=user.id)
                    # send email only if configuration is set
                    if settings.EMAIL_HOST_EXIST is not None :
                        html_content = render_to_string(Words.update_pass_temp,
                                                        {
                            'username': f"{user.first_name} {user.last_name}",
                            'website_url': settings.ALLOWED_HOSTS[0],
                            'website_name': settings.WEBISTE_NAME
                                                        }
                                                        )
                        send_mail(subject="PASSWORD HAS BEEN CHANGED", recipient_list=[user.email],
                                  html_message=html_content, from_email=settings.DEFAULT_FROM_EMAIL,
                                  message=strip_tags(html_content))
                    return redirect("/",permanent=True)
                else:
                    return render(request, Words.update_pass_url, {"form": form})
            else:
                form.add_error("password", tran.gettext("Both passwords are not same"))
                return render(request, Words.update_pass_url, {"form": form})
        else:
            return render(request, Words.update_pass_url, {"form": form})


from .tasks import add

def test_cel():
    results = add.delay(4,4)
    print(results)