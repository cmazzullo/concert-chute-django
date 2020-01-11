from django.test import TestCase
from django.conf import settings

from unittest import mock

from datetime import datetime, date

PAGE_1 = {
    'last_item': None,
    'total_items': '3',
    'first_item': None,
    'page_number': '1',
    'page_size': '1',
    'page_items': None,
    'search_time': '0.075',
    'page_count': '2',
    'events': {
        'event': [
            {
                'url': 'http://event.com',
                'id': 'E0-001-126398343-6@2019112723',
                'city_name': 'Washington',
                'country_name': 'United States',
                'region_name': 'District of Columbia',
                'start_time': '2019-11-27 23:00:00',
                'description': 'blah',
                'title': 'Abby Wednesdays',
                'venue_address': '1730 M Street Northwest',
                'recur_string': 'on various days',
                'venue_id': 'V0-001-014295567-2',
                'venue_name': 'Abigail Nightclub',
                'venue_url': 'blah.com',
            },
        ]
    }
}

PAGE_2 = {
    'last_item': None,
    'total_items': '3',
    'first_item': None,
    'page_number': '2',
    'page_size': '2',
    'page_items': None,
    'search_time': '0.075',
    'page_count': '2',
    'events': {
        'event': [
            {
                'url': 'blah.com',
                'id': 'E0-001-118686410-6@2019112623',
                'city_name': 'Washington',
                'country_name': 'United States',
                'region_name': 'District of Columbia',
                'start_time': '2019-11-26 23:00:00',
                'description': 'blah',
                'title': 'Saint Yves Nightclub',
                'venue_address': '1220 Connecticut Avenue Northwest',
                'recur_string': 'on various days',
                'venue_id': 'V0-001-011925669-8',
                'venue_name': 'Saint Yves',
                'venue_url': 'blah.com'
            },
            {
                'url': 'blah.com',
                'id': 'E0-001-125746491-2@2019112718',
                'city_name': 'Washington',
                'country_name': 'United States',
                'region_name': 'District of Columbia',
                'start_time': '2019-11-27 18:00:00',
                'description': ' Singer-Songwriter Open Mic',
                'title': 'Singer-Songwriter Open Mic at Hellbender',
                'venue_address': '5788 2nd Street Northeast',
                'recur_string': 'on various days',
                'venue_id': 'V0-001-009178563-0',
                'venue_name': 'Hellbender Brewing Company',
                'venue_url': 'http://venue.com'
            },
        ]
    }
}

from ..utils import (
    CONCERT_TO_JSON_MAP,
    VENUE_TO_JSON_MAP,
    json_to_models,
    format_daterange,
    clean_raw_page,
    get_all_query_data,
    format_date_for_api,
    get_query_page,
    BASE_URL,
    get_json,
    get_page_count
)


class TestUtils(TestCase):
    def setUp(self):
        self.params = {
            'app_key': settings.EVENTFUL_API_KEY,
            'location': 'washington dc',
            'date': '2019010100-2019010100',
            'category': 'music',
            'page_size': '1',
        }

    def test_format_date_for_api(self):
        "API wants date that look like this: 2019112700"
        self.assertEqual(
            format_date_for_api(date(2019, 1, 1)),
            "2019010100"
        )

    @mock.patch('requests.get')
    def test_get_query_page(self, mock_get):
        get_query_page(self.params, 1)
        mock_get.assert_called_once_with(
            BASE_URL,
            params={'page_number': 1, **self.params}
        )

    @mock.patch('requests.get')
    def test_get_json(self, mock_get):
        get_json(self.params)
        mock_get.assert_called_once_with(
            BASE_URL,
            params=self.params,
        )

    @mock.patch('concert_chute_django.core.utils.get_json')
    def test_get_all_query_data(self, mock_get_json):
        # Return PAGE_1 for the first call, PAGE_2 for the second:
        mock_get_json.side_effect = [PAGE_1, PAGE_2]
        self.assertEqual(
            get_all_query_data(self.params),
            PAGE_1['events']['event'] + PAGE_2['events']['event'],
        )

    def test_get_page_count(self):
        self.assertEqual(get_page_count(PAGE_1), 2)

    def test_clean_raw_page(self):
        self.assertEqual(
            clean_raw_page(PAGE_1),
            PAGE_1['events']['event'],
        )

    def test_format_daterange(self):
        self.assertEqual(
            format_daterange(date(2019, 5, 6), date(2020, 1, 2)),
            '2019050600-2020010200',
        )

    def test_json_to_models(self):
        json = {
            'url': 'http://event.com',
            'id': 'E0-001-126398343-6@2019112723',
            'city_name': 'Washington',
            'country_name': 'United States',
            'region_name': 'District of Columbia',
            'start_time': '2019-11-27 23:00:00',
            'description': None,
            'title': 'Abby Wednesdays',
            'venue_address': '1730 M Street Northwest',
            'recur_string': None,
            'venue_id': 'V0-001-014295567-2',
            'venue_name': 'Abigail Nightclub',
            'venue_url': 'blah.com',
        }
        concert, venue = json_to_models(json)

        for model_field, json_field in CONCERT_TO_JSON_MAP:
            self.assertEqual(getattr(concert, model_field), json[json_field])

        for model_field, json_field in VENUE_TO_JSON_MAP:
            self.assertEqual(getattr(venue, model_field), json[json_field])

        venue.save()
        concert.save()
        self.assertEqual(concert.venue, venue)
