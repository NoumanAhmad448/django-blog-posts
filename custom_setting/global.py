from django.conf import settings

class Global:
    available_langs = [settings.LANGUAGE_CODE, "ch"]
