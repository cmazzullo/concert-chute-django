from django.test import TestCase

from model_bakery import baker

from concert_chute_django.core.models import Concert


class ModelTest(TestCase):
    def test_concert_model_crash(self):
        Concert.objects.all()

    def test_make_venue_and_concert(self):
        venue = baker.make('core.Venue')
        concert = baker.make('core.Concert', venue=venue)
        self.assertEqual(concert.venue, venue)
