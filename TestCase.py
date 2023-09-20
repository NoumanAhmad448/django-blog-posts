from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail

class TestCase(TestCase):
    def setUp(self,is_sup_user_login=False):
        self.credentials = {
            "username" : settings.DATABASES["default"]["TEST"]["TEST_EMAIL"],
            "super_username" : f'super_{settings.DATABASES["default"]["TEST"]["TEST_EMAIL"]}',
            "super_email" : f'super_{settings.DATABASES["default"]["TEST"]["TEST_EMAIL"]}',
            "email" : f'super_{settings.DATABASES["default"]["TEST"]["TEST_EMAIL"]}',
            "password": settings.DATABASES["default"]["TEST"]["TEST_PASS"],
            "wrong_password": "wrong_pass"
        }
        self.post_ob ={
                    "source": "api",
                    "title": "lorem ipsum lorem ipsum",
                    "tags": "t1,t2,t3,t4,t5",
                    "descrip": "lorem ipsum",
                    "should_display": True,
        }
        if is_sup_user_login:
            user = User.objects.create_superuser(username=self.credentials["super_username"],email=self.credentials["super_email"])
        else:
            user = User.objects.create(username=self.credentials["username"],email=self.credentials["email"])

        user.set_password(self.credentials["password"])
        user.save()

        if is_sup_user_login:
            self.client.login(username=self.credentials["super_username"],password=self.credentials["password"])
        else:
            self.client.login(username=self.credentials["username"],password=self.credentials["password"])

        # set email outbox empty
        mail.outbox = []
