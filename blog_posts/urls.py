from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _

admin.site.site_header = _('Blog Post Writer')
admin.site.site_title = _('blog post writer')

urlpatterns = [
    path("", include('auths.urls')),
    path('api/', include("api_v1.urls")),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('blogs/', include('blogs.urls')),
]