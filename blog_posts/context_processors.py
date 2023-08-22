from django.conf import settings

def global_setting(request):
    return {'DEBUG': settings.DEBUG}