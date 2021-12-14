from actstream import action
from actstream.models import Action
from django.contrib.auth.models import User
from prophecies.core.models.choice import Choice
from prophecies.core.models.choice_group import ChoiceGroup

from django.test import TestCase
from rest_framework.test import APIClient
import time_machine
import datetime as dt


class TestActionAggregation(TestCase):
    client = APIClient()
    fixtures = ['users.json']


    def setUp(self):
        self.olivia = User.objects.get(username='olivia')
        self.django = User.objects.get(username='django')

    # TODO : rename day -> date
    # TODO : rename aggregation -> aggregate
    def test_create_aggregated_action_post_save_on_action(self):
        action.send(self.olivia, verb='added', target=self.django)
        self.client.login(username='olivia', password='olivia')

        request = self.client.get('/api/v1/action-aggregations/')
        action_aggregations = request.json().get('data')
        self.assertEqual(len(action_aggregations),1)

        first_aggregate_attributes= action_aggregations[0].get('attributes')
        self.assertEqual(first_aggregate_attributes.get('count'),1)

    def test_update_aggregated_action_using_streams(self):
        action.send(self.olivia, verb='added', target=self.django)
        action.send(self.olivia, verb='added', target=self.django)
        self.client.login(username='olivia', password='olivia')

        request = self.client.get('/api/v1/action-aggregations/')
        action_aggregations = request.json().get('data')
        self.assertEqual(len(action_aggregations),1)
        first_aggregate_attributes= action_aggregations[0].get('attributes')
        self.assertEqual(first_aggregate_attributes.get('count'),2)

    def test_list_returns_all_action_aggregations(self):
        action.send(self.olivia, verb='follow', target=self.django)
        action.send(self.olivia, verb='unfollow', target=self.django)
        action.send(self.olivia, verb='follow', target=self.django)
        action.send(self.olivia, verb='unfollow', target=self.django)

        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/action-aggregations/')
        self.assertEqual(request.status_code, 200)
        self.assertEqual(len(request.json().get('data')), 2)

    def test_the_user_relationship_exists(self):
        action.send(self.olivia, verb='follow', target=self.django)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/action-aggregations/')
        data = request.json().get('data')
        relationships = data[0].get('relationships')
        self.assertEqual(relationships['actor']['data']['id'], str(self.olivia.id))

    def test_aggregate_on_two_days(self):
        with time_machine.travel(0, tick=False) as traveller:
            action.send(self.olivia, verb='follow', target=self.django)
            traveller.shift(dt.timedelta(days=1))
            action.send(self.olivia, verb='follow', target=self.django)
        self.client.login(username='olivia', password='olivia')
        request = self.client.get('/api/v1/action-aggregations/')
        self.assertEqual(len(request.json().get('data')), 2)

    def test_aggregates_only_actions_from_user_actor_content_type(self):
        action.send(self.olivia, verb='added', target=self.django)
        choice_group = ChoiceGroup.objects.create(name='Is it correct?')
        choice = Choice.objects.create(name='Yes', choice_group=choice_group)
        action.send(choice, verb='added', target=self.django)
        self.assertEqual(len(Action.objects.filter_actor_content_type('user')), 1)

    def test_error_raise_when_actor_content_type_is_not_a_known_model_name(self):
        with self.assertRaises(ValueError):
            Action.objects.filter_actor_content_type('User')