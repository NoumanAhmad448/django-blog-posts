from django.utils import translation as tran

class LanguageTransMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        LANGUAGE_CODE = 'en'
        get_req = request.GET.copy()
        lang = get_req.get('lang', None)
        language = lang if lang is not None else LANGUAGE_CODE
        get_req['lang'] = language
        tran.activate(language)
        response = self.get_response(request)

        return response