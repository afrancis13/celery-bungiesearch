from datetime import datetime

import pytz
from bungiesearch import Bungiesearch
from bungiesearch.signals import get_signal_processor
from celery_bungiesearch import CelerySignalProcessor
from celery_bungiesearch.tasks import BulkDeleteTask, CeleryBungieTask
from django.core.management import call_command
from django.test import TestCase

from core.models import User

signal_processor = get_signal_processor()


class SignalTest(TestCase):

    def setUp(self):
        self.updated = pytz.UTC.localize(datetime(year=2015, month=6, day=1))
        call_command('search_index', action='create')

    def tearDown(self):
        call_command('search_index', action='delete', confirmed='guilty-as-charged')

    def assertResultsLength(self, results, expected):
        length = len(results)
        msg = 'Search did not return exactly %s items (got %s)' % (expected, length)
        self.assertEqual(length, expected, msg)

    def test_signal_processor(self):
        self.assertTrue(isinstance(signal_processor, CelerySignalProcessor),
            'signal_processor is not an instance of CelerySignalProcessor')

    def test_force_refresh(self):
        jane_doe = {
            'name': 'Jane Doe',
            'user_id': 'jdoe1',
            'updated': self.updated
        }

        previous = CeleryBungieTask.refresh
        try:
            CeleryBungieTask.refresh = True
            user = User.objects.create(**jane_doe)
        finally:
            CeleryBungieTask.refresh = previous

        result = User.objects.search.query('match', name='Jane')
        self.assertEqual(len(result), 1)

        BulkDeleteTask().delay(User, [user.pk], refresh=True)
        result = User.objects.search.query('match', name='Jane')
        self.assertEqual(len(result), 0)

    def test_save(self):
        error_message_len = (lambda w, x, y, z:
            'Searching for {} in {} did not return {} results (got {})'.format(w, x, y, z))

        error_message_contains = (lambda w, x, y, z:
            'Searching for {} in {} did not return the name {} (got {})'.format(w, x, y, z))

        jane_doe = {
            'name': 'Jane Doe',
            'user_id': 'jdoe1',
            'updated': self.updated
        }
        john_doe = {
            'name': 'John Doe',
            'user_id': 'jdoe2',
            'updated': self.updated
        }
        cryptography = {
            'name': 'Bob Alice Eve',
            'user_id': 'bae',
            'updated': self.updated
        }

        User.objects.create(**jane_doe)
        Bungiesearch().get_es_instance().indices.refresh()

        single_result_check = User.objects.search.query('match', name='Doe')

        self.assertEqual(len(single_result_check), 1,
            error_message_len('Doe', 'name', 1, len(single_result_check)))
        self.assertEqual(single_result_check[0].name, 'Jane Doe',
            error_message_contains('Doe', 'name', 'Jane Doe', single_result_check[0].name))

        User.objects.create(**john_doe)
        Bungiesearch().get_es_instance().indices.refresh()

        two_result_check = User.objects.search.query('match', _all='doe')
        self.assertEqual(len(two_result_check), 2,
            error_message_len('Doe', 'user_id', 2, len(two_result_check)))

        User.objects.create(**cryptography)
        Bungiesearch().get_es_instance().indices.refresh()

        no_additional_result_check = User.objects.search.query('match', name='Doe')
        single_result_check = User.objects.search.query('match', name='Alice')
        self.assertEqual(len(no_additional_result_check), 2,
            error_message_len('Doe', 'name', 2, len(no_additional_result_check)))
        self.assertEqual(len(single_result_check), 1,
            error_message_len('Alice', 'name', 1, len(single_result_check)))
        self.assertEqual(single_result_check[0].name, 'Bob Alice Eve',
            error_message_contains('Alice', 'name', 'Bob Alice Eve', single_result_check[0].name))

    def test_delete(self):
        clinton = {
            'name': 'Bill Clinton',
            'user_id': 'clinton42',
            'updated': self.updated
        }
        obama = {
            'name': 'Barack Obama',
            'user_id': 'obama44',
            'updated': self.updated
        }
        bush = {
            'name': 'George W. Bush',
            'user_id': 'bush43',
            'updated': self.updated
        }

        first_user = User.objects.create(**clinton)
        second_user = User.objects.create(**obama)
        third_user = User.objects.create(**bush)
        Bungiesearch().get_es_instance().indices.refresh()

        search_all = User.objects.search.query('match', updated=self.updated)

        self.assertEqual(len(search_all), 3,
            'Search did not return exactly 3 users (got {})'.format(len(search_all)))
        first_user.delete()
        Bungiesearch().get_es_instance().indices.refresh()

        self.assertEqual(len(search_all), 2,
            'Search did not return exactly 2 users (got {})'.format(len(search_all)))
        second_user.delete()
        Bungiesearch().get_es_instance().indices.refresh()

        self.assertEqual(len(search_all), 1,
            'Search did not return exactly 1 user (got {})'.format(len(search_all)))
        third_user.delete()
        Bungiesearch().get_es_instance().indices.refresh()

        self.assertEqual(len(search_all), 0,
            'Search did not return exactly 0 users (got {})'.format(len(search_all)))

    def test_save_and_delete(self):
        berkeley = {
            'name': 'UC Berkeley',
            'user_id': 'ucb',
            'updated': self.updated
        }
        stanford = {
            'name': 'Stanford',
            'user_id': 'tree',
            'updated': self.updated
        }

        first_user = User.objects.create(**berkeley)
        Bungiesearch().get_es_instance().indices.refresh()

        search_all = User.objects.search.query('match', updated=self.updated)

        self.assertEqual(len(search_all), 1,
            'Search did not return exactly 1 user (got {})'.format(len(search_all)))

        second_user = User.objects.create(**stanford)
        Bungiesearch().get_es_instance().indices.refresh()

        self.assertEqual(len(search_all), 2,
            'Search did not return exactly 2 users (got {})'.format(len(search_all)))

        second_user.delete()
        Bungiesearch().get_es_instance().indices.refresh()

        self.assertEqual(len(search_all), 1,
            'Search did not return exactly 1 user (got {})'.format(len(search_all)))

        empty_set_check = User.objects.search.query('match', name='Stanford')
        self.assertEqual(len(empty_set_check), 0,
            'Searching for Stanford did not return 0 users (got {})'.format(len(empty_set_check)))

        first_user.user_id = 'Beat Stanford'
        first_user.save()
        Bungiesearch().get_es_instance().indices.refresh()

        self.assertEqual(len(User.objects.search.query('match', _all='Beat Stanford')), 1,
            'Search did not return exactly 1 user (got {})'.format(len(search_all)))
        self.assertEqual(search_all[0].user_id, 'Beat Stanford',
            'Search did not return user with user_id Beat Stanford (got {})'
            .format(search_all[0].user_id))

        first_user.delete()
        Bungiesearch().get_es_instance().indices.refresh()

        self.assertEqual(len(search_all), 0,
            'Search did not return exactly 1 user (got {})'.format(len(search_all)))

    def test_bulk_delete(self):
        peanut_butter = {
            'name': 'Peanut Butter',
            'user_id': 'pb',
            'updated': self.updated
        }
        peanut_butter_and_jelly = {
            'name': 'Peanut Butter & Jelly',
            'user_id': 'pbjelly',
            'updated': self.updated
        }

        first_user = User.objects.create(**peanut_butter)
        second_user = User.objects.create(**peanut_butter_and_jelly)
        Bungiesearch().get_es_instance().indices.refresh()

        two_result_check = User.objects.search.query('match', name='Peanut')
        self.assertResultsLength(two_result_check, 2)

        model_item_pks = [first_user.pk, second_user.pk]
        BulkDeleteTask().delay(User, model_item_pks)
        Bungiesearch().get_es_instance().indices.refresh()

        empty_set_check = User.objects.search.query('match', name='Peanut')
        self.assertResultsLength(empty_set_check, 0)

    def test_indexing_queryset(self):
        fake = {
            'name': 'fraud',
            'user_id': 'fake',
            'updated': self.updated,
        }
        discovered = {
            'name': 'fraud',
            'user_id': 'real',
            'updated': self.updated
        }

        User.objects.create(**fake)
        discovered_user = User.objects.create(**discovered)
        Bungiesearch().get_es_instance().indices.refresh()

        # Check to ensure that user_id fake is excluded as dictated by index_queryset
        one_result_check = User.objects.search.query('match', name='fraud')
        self.assertEqual(len(one_result_check), 1,
            'Search did not return exactly 1 user (got {})'.format(len(one_result_check)))

        discovered_user.user_id = 'fake'
        discovered_user.save()
        Bungiesearch().get_es_instance().indices.refresh()

        # Check to ensure same result on a change and save operation
        empty_set_check = User.objects.search.query('match', name='fraud')
        self.assertEqual(len(empty_set_check), 0,
            'Search did not return exactly 0 users (got {})'.format(len(empty_set_check)))
