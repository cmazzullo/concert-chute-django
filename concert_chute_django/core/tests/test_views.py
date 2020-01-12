from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse

from model_bakery import baker

from concert_chute_django.core.utils import upcoming_concerts


class HomeTest(TestCase):
    def test_home_does_not_crash(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_gets_concerts(self):
        "View should show future concerts but not past concerts."
        baker.make('core.Concert', start_time=datetime.now() - timedelta(1))
        baker.make('core.Concert', start_time=datetime.now() + timedelta(1))
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['concerts']), 1)
        self.assertQuerysetEqual(
            response.context['concerts'],
            [repr(concert) for concert in upcoming_concerts()],
        )


class VenueTest(TestCase):
    def test_view_venue(self):
        venue = baker.make('core.Venue')
        response = self.client.get(reverse('view_venue', args=[venue.pk]))
        self.assertEqual(response.context['venue'], venue)
