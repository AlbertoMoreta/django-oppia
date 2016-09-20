from django.test import TestCase
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCaseMixin

from oppia.tests.utils import getApiKey


class BadgesResourceTest(ResourceTestCaseMixin, TestCase):
    fixtures = ['user.json', 'oppia.json', 'default_badges.json']

    def setUp(self):
        super(BadgesResourceTest, self).setUp()
        user = User.objects.get(username='demo')
        api_key = getApiKey(user=user)
        self.auth_data = {
            'username': 'demo',
            'api_key': api_key.key,
        }
        self.url = '/api/v1/badges/'

     # check post not allowed
    def test_post_invalid(self):
        self.assertHttpMethodNotAllowed(self.api_client.post(self.url, format='json', data={}))

    # check unauthorized
    def test_unauthorized(self):
        data = {
            'username': 'demo',
            'api_key': '1234',
        }
        self.assertHttpUnauthorized(self.api_client.get(self.url, format='json', data=data))

    # check correct
    def test_correct(self):
        resp = self.api_client.get(self.url, format='json', data=self.auth_data)
        self.assertHttpOK(resp)
        self.assertValidJSON(resp.content)

        # check that the response contains 2 badges
        response_data = self.deserialize(resp)
        self.assertTrue('objects' in response_data)
        self.assertEquals(len(response_data['objects']),2)
