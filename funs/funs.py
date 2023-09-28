def get_client_ip(request):
    ip = request.META.get('REMOTE_ADDR')
    if ip is None:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0]

    return ip