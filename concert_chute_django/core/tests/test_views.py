from django.test import TestCase

from concert_chute_django.core.views import home


class HomeTest(TestCase):
    def test_home_does_not_crash(self):
        request = self.client.get('/')
        home(request)
