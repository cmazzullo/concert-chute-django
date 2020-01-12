from datetime import date, timedelta

from concert_chute_django.core.utils import (
    json_to_models,
    format_daterange,
    format_date_for_api,
    get_all_query_data,
    DEFAULT_PARAMS
)

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    help = 'Download concert data from the Eventful API'

    def get_data(self):
        return get_all_query_data({
            'date': format_daterange(date.today(), date.today() + timedelta(35)),
            **DEFAULT_PARAMS
        })

    def handle(self, *args, **options):
        data = self.get_data()
        models = [json_to_models(event) for event in data]
        for concert, venue in models:
            venue.save()
            concert.save()

        self.stdout.write(self.style.SUCCESS(f'{len(models)} concerts saved'))
