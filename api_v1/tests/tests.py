from django.test import TestCase
from django.urls import reverse
from rest_framework import status as http_status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import json
from django.contrib.auth.models import User


class APIV1TestCase(TestCase):
    def setUp(self):
        self.credentials = {
            "email" : settings.DATABASES["default"]["TEST"]["TEST_EMAIL"],
            "password": settings.DATABASES["default"]["TEST"]["TEST_PASS"]
        }
        user = User.objects.create(username=self.credentials["email"])
        user.set_password(self.credentials["password"])
        user.save()

    def test_user_not_auth(self):
        self.credentials["password"] = f"{self.credentials['password']}wrongpassword"
        resp = self.client.post(reverse("create_token"),
                                json.dumps(self.credentials),
                                content_type="application/json")
        self.assertEqual(resp.status_code, http_status.HTTP_400_BAD_REQUEST)
