from django.test import TestCase
from django.utils.crypto import get_random_string
import random
from django.urls import reverse
from rest_framework import status as http_status

from api_v1.models.create_post_model import CreatePostModel
class CreatePostModelTestCase(TestCase):

    def test_create_post(self):
        createPost = CreatePostModel()
        createPost.title = get_random_string(length=500)
        createPost.source = createPost.POST_CHOICES[0][0]
        createPost.tags = get_random_string(length=500)
        createPost.descrip = get_random_string(length=1000)
        createPost.should_display = random.choice([True,False])
        createPost.save()
        self.assertEquals(createPost.id,createPost.id)

    def test_update_post(self):
        createPost = CreatePostModel()
        createPost.title = get_random_string(length=500)
        createPost.source = createPost.POST_CHOICES[0][0]
        createPost.tags = get_random_string(length=500)
        createPost.descrip = get_random_string(length=1000)
        createPost.should_display = random.choice([True,False])
        createPost.save()
        self.create_post = createPost

        source_api = self.create_post.POST_CHOICES[0][1]
        self.create_post.source = source_api
        self.create_post.save()
        self.assertEquals(self.create_post.source,source_api)


    def test_latest_posts(self):
        resp = self.client.get(reverse("latest_posts"))
        self.assertEqual(resp.status_code,http_status.HTTP_200_OK)

    def test_create_posts(self):
        resp = self.client.get(reverse("create-post"))
        self.assertEqual(resp.status_code,http_status.HTTP_302_FOUND)
        self.assertRedirects(resp,expected_url=reverse("login_user")+"?next="+reverse("create-post"))

