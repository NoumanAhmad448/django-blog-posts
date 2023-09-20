from TestCase import TestCase
from django.urls import reverse
from rest_framework import status as http_status
from django.conf import settings
from django.test import tag
from django.core import mail
from unittest import skipIf
@tag("slow")
class UserAuthTestCase(TestCase):
    def setUp(self):
        super().setUp()

    @tag("test_update_pass")
    def test_update_pass(self):
        self.credentials["password"] = f'{self.credentials["password"]}'
        self.credentials["c_password"] = f'{self.credentials["password"]}'

        resp = self.client.post(reverse("update_password"),self.credentials)
        self.assertEqual(resp.status_code, http_status.HTTP_301_MOVED_PERMANENTLY)
        if mail.outbox.__len__() > 0:
            self.assertEqual(mail.outbox[0].from_email,settings.DEFAULT_FROM_EMAIL)
            self.assertEqual(mail.outbox[0].subject, "PASSWORD HAS BEEN CHANGED")
            if mail.outbox[0].to.__len__() > 0:
                self.assertEqual(mail.outbox[0].to[0], self.credentials["email"])

    @tag("test_update_pass_validation")
    def test_update_pass_validation(self):

        resp = self.client.post(reverse("update_password"),self.credentials)
        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)

    @tag("test_update_pass_miss_match")
    def test_update_pass_miss_match(self):
        self.credentials["password"] = f'{self.credentials["password"]}'
        self.credentials["c_password"] = f'{self.credentials["password"]}lfdjal;fjd;lfja;djf;dfjdl;'

        resp = self.client.post(reverse("update_password"),self.credentials)
        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)

    @tag("test_update_pass_get")
    def test_update_pass_get(self):
        resp = self.client.get(reverse("update_password"))
        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)

    @tag("skip_test")
    @skipIf(False,reason="testing")
    def skip_test(self):
        pass
