from datetime import datetime, timedelta
from itertools import chain

from django.conf import settings

import requests

from .models import Concert, Venue

BASE_URL = 'https://api.eventful.com/json/events/search'
DEFAULT_PARAMS = {
    'app_key': settings.EVENTFUL_API_KEY,
    'location': 'washington dc',
    'category': 'music',
}


def format_daterange(start_date, end_date):
    return (
        format_date_for_api(start_date) + '-' +
        format_date_for_api(end_date)
    )


def get_json(params):
    "Make a GET request and return the JSON data of the response."
    return requests.get(BASE_URL, params=params).json()


def get_query_page(params, page):
    "Download a page of data for a query and return it as JSON."
    return get_json({'page_number': page, **params})


def get_all_query_data(params):
    "Download all pages of data for a query and return them as a JSON object."
    first_page = get_query_page(params, 1)
    rest_pages = [get_query_page(params, page)
                  for page in range(2, get_page_count(first_page) + 1)]
    pages = [first_page] + rest_pages
    return list(chain.from_iterable(map(clean_raw_page, pages)))


def format_date_for_api(dt):
    return dt.strftime("%Y%m%d00")


def get_page_count(raw_page):
    "Extract page_count from the raw API json"
    return int(raw_page['page_count'])


def clean_raw_page(raw_page):
    """
    Turn a raw JSON page from the API into a list of Events.

    Cleaned data looks like:
    [{'event_title': 'mytitle', 'event_url': 'myurl.com'},
     {'event_title': 'title2',  'event_url': 'otherurl.com'}]
    """
    try:
        return raw_page['events']['event']
    except KeyError:
        return []


CONCERT_TO_JSON_MAP = [
    ('eventful_id', 'id'),
    ('title', 'title'),
    ('description', 'description'),
    ('url', 'url'),
    ('start_time', 'start_time'),
    ('recur_string', 'recur_string'),
]

VENUE_TO_JSON_MAP = [
    ('eventful_id', 'venue_id'),
    ('name', 'venue_name'),
    ('url', 'venue_url'),
    ('city', 'city_name'),
    ('country', 'country_name'),
    ('region', 'region_name'),
    ('address', 'venue_address'),
]


def json_to_models(event_json):
    "Turn raw data from the API into Concert and Venue models."
    concert = Concert()
    for model_field, json_field in CONCERT_TO_JSON_MAP:
        setattr(concert, model_field, event_json[json_field])

    venue = Venue()

    for model_field, json_field in VENUE_TO_JSON_MAP:
        setattr(venue, model_field, event_json[json_field])

    concert.venue = venue
    return concert, venue


def upcoming_concerts():
    return Concert.objects.filter(
        start_time__gte=datetime.now(),
        start_time__lte=datetime.now() + timedelta(30),
    )
