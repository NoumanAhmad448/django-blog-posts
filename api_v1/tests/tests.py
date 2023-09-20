from django.urls import reverse
from rest_framework import status as http_status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import json
from django.contrib.auth.models import User
from api_v1.generic_funs import ApiResponse
from api_v1.models.create_post_model import CreatePostModel
from  TestCase import TestCase

class APIV1TestCase(TestCase):
    def setUp(self):
        super().setUp(is_sup_user_login=True)
        self.post_ob ={
            "source": "api",
            "title": "lorem ipsum lorem ipsum",
            "tags": "t1,t2,t3,t4,t5",
            "descrip": "lorem ipsum",
            "should_display": True,
        }

    def test_user_post_validation(self):
        api_resp = ApiResponse()
        self.post_ob["source"] = ""
        resp = self.client.post(reverse("create_post"),self.post_ob)
        ac_resp = json.loads(resp.content.decode())

        self.assertEqual(resp.status_code, http_status.HTTP_400_BAD_REQUEST)
        self.assertEqual(ac_resp[api_resp.IS_SUCCESS], False)

    def test_user_post(self):
        api_resp = ApiResponse()
        post_model = CreatePostModel()

        resp = self.client.post(reverse("create_post"),self.post_ob)
        ac_resp = json.loads(resp.content.decode())

        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)
        self.assertEqual(ac_resp[api_resp.IS_SUCCESS], True)

        id = ac_resp[api_resp.DATA][post_model.ID]
        self.post_ob[post_model.ID] = id
        resp = self.client.post(reverse("create_post"),self.post_ob)
        ac_resp = json.loads(resp.content.decode())

        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)
        self.assertEqual(ac_resp[api_resp.IS_SUCCESS], True)

    def test_user_post_json(self):
        api_resp = ApiResponse()
        post_model = CreatePostModel()

        resp = self.client.post(reverse("create_post"),json.dumps(self.post_ob),
                                content_type="application/json")
        ac_resp = json.loads(resp.content.decode())

        self.assertEqual(resp.status_code, http_status.HTTP_200_OK)
        self.assertEqual(ac_resp[api_resp.IS_SUCCESS], True)
        self.assertEqual(ac_resp[api_resp.DATA][post_model.SOURCE], self.post_ob["source"])

    def test_user_not_auth(self):
        self.credentials["password"] = f"{self.credentials['wrong_password']}"
        resp = self.client.post(reverse("create_token"),
                                json.dumps(self.credentials),
                                content_type="application/json")
        self.assertEqual(resp.status_code, http_status.HTTP_400_BAD_REQUEST)


