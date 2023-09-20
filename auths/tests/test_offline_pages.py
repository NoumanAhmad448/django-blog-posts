from django.test import TestCase
from django.urls import reverse
from rest_framework import status as http_status
from django.conf import settings
from auths.keywords.html_page import HtmlPage as Words
from django.test import tag

@tag("slow")
class OfflinePages(TestCase):
    credentials = {
        "email" : settings.DATABASES["default"]["TEST"]["TEST_EMAIL"],
        "password": settings.DATABASES["default"]["TEST"]["TEST_PASS"]
    }
    def test_user_register_page(self):
        resp = self.client.get(reverse("register_user"))
        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)
        if resp.templates is not None and resp.templates.__len__()>0:
            self.assertEqual(resp.templates[0].name, Words.reg_url)

    @tag("test_user_register_page_lang")
    def test_user_register_page_lang(self):
        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "zh"})
        resp = self.client.get(reverse("register_user"))
        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)
        if resp.templates is not None and resp.templates.__len__()>0:
            self.assertEqual(resp.templates[0].name, Words.reg_url)

    def test_user_login(self):
        resp = self.client.post(reverse("login_user"),self.credentials)
        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)

