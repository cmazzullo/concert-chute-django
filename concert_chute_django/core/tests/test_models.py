from django.test import TestCase

from concert_chute_django.core.models import Concert


class ModelTest(TestCase):
    def test_concert_model_crash(self):
        Concert.objects.all()
