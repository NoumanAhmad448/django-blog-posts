from TestCase import TestCase
from django.test import tag
from io import StringIO
from django.core.management import call_command

@tag("slow")
class CustomCommands(TestCase):
    def setUp(self):
        super().setUp()

    @tag("test_dev_command")
    def test_dev_command(self):
        # out = StringIO()
        # call_command("dev")
        # self.assertIn(True)
        pass
