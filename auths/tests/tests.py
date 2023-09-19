from django.test import TestCase
from django.urls import reverse
from rest_framework import status as http_status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
class UserAuthTestCase(TestCase):
    credentials = {
            "email" : settings.DATABASES["default"]["TEST"]["TEST_EMAIL"],
            "password": settings.DATABASES["default"]["TEST"]["TEST_PASS"]
        }

    @method_decorator(csrf_exempt)
    def test_user_login(self):
        resp = self.client.post(reverse("login_user"),self.credentials)
        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)