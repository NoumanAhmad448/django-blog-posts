def get_client_ip(request):
    ip = request.META.get('REMOTE_ADDR')
    if ip is None:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0]

    return ip

def get_current_lang(request):
    return request.GET.get("lang") if request.GET.get("lang") else "en"

def get_alt_lang(request):
    return 'zh' if get_current_lang(request) == 'en' else 'en'
