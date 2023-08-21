from django.utils import translation as tran

class LanguageTransMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get('lang')
        language = lang if lang is not None else "en"
        tran.activate(language)
        response = self.get_response(request)

        return response