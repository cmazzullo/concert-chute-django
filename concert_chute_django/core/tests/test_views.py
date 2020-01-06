from django.test import TestCase
from django.urls import reverse


class HomeTest(TestCase):
    def test_home_does_not_crash(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_gets_concerts(self):
        from concert_chute_django.core.models import Concert
        response = self.client.get(reverse('home'))
        self.assertQuerysetEqual(
            response.context['concerts'],
            Concert.objects.all()
        )
