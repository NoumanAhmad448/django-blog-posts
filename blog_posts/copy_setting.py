"""
Django settings for blog_posts project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv
import json

load_dotenv()
env = os.environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+62!vb(g7$zte*go8t_&89(kf$y!h^3vpq2@7#a=mm@$@q0o#='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = json.loads(env.get("ALLOWED_HOSTS"))
WEBISTE_NAME="blog posts"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blogs.apps.BlogsConfig',
    'auths.apps.AuthsConfig',
    'api_v1.apps.ApiV1Config',
    'rest_framework',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'rest_framework.authtoken'
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middlewares.LanguageTransMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

ROOT_URLCONF = 'blog_posts.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog_posts.context_processors.global_setting',
            ],
        },
    },
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [
            "/home/html/jinja2",
        ],
    },
]

WSGI_APPLICATION = 'blog_posts.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
     "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.get("DEFAULT_DATABASE_NAME"),
        "USER": env.get("DEFAULT_DATABASE_USERNAME"),
        "PASSWORD": env.get("DEFAULT_DATABASE_PASSWORD"),
        "HOST": env.get("DEFAULT_DATABASE_HOST"),
        "PORT": env.get("DEFAULT_DATABASE_PORT"),
        "TEST": {
            "NAME": env.get("DEFAULT_TEST_DATABASE_NAME"),
            "TEST_PASS": env.get("TEST_PASS"),
            "TEST_EMAIL": env.get("TEST_EMAIL")
        },
     },
     "default01": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env.get("DEFAULT_DATABASE_NAME"),
        "USER": env.get("DEFAULT_DATABASE_USERNAME"),
        "PASSWORD": env.get("DEFAULT_DATABASE_PASSWORD"),
        "HOST": env.get("DEFAULT_DATABASE_HOST"),
        "PORT": env.get("DEFAULT_DATABASE_PORT"),
        "TEST": {
            "NAME": env.get("DEFAULT_TEST_DATABASE_NAME")
        },
    },
     "live": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "usmansaleem234_django_blog_posts",
        "USER": "django_blog_posts",
        "PASSWORD": "django_blog_posts",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# changing the language_code value required a value to be changed in LanguageTransMiddleware
LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'assets/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ]
}

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

LANGUAGES =[ ('en', _('English')),
    ('zh', _('Chinese'))]

SITE_ROOT = os.path.dirname(os.path.realpath(__name__))

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

STATICFILES_DIRS =  [ os.path.join(BASE_DIR,'static')]

LOCALE_PATHS = ( os.path.join(SITE_ROOT, 'locale'), )

DATE_FORMAT="d F Y"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "debug.log",
            },
            "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "email_backend": "django.core.mail.backends.filebased.EmailBackend",
            "include_html": True,
        }
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

ADMINS=[("Nouman Ahamd", "your_email@django-mail.com")]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env.get("REDIS_LOCATION"),
        "KEY_PREFIX": "wiki",
        "TIMEOUT": env.get("REDIS_TIMEOUT"),
        # "LOCATION": "redis://username:password@127.0.0.1:6379",
    }
}

# send email only if configuration is set
EMAIL_HOST_EXIST=True #if this is not set to true email will not be fired
EMAIL_HOST=env.get("EMAIL_HOST")
EMAIL_HOST_PASSWORD=env.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER=env.get("EMAIL_HOST_USER")
EMAIL_PORT=env.get("EMAIL_PORT")
DEFAULT_FROM_EMAIL=env.get("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS=True

AUTHENTICATION_BACKENDS=["django.contrib.auth.backends.ModelBackend"]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_DOMAIN='localhost:8080'

