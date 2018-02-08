import json
from tornado.testing import AsyncHTTPTestCase

from event_machine import server


class TestServer(AsyncHTTPTestCase):
    def get_app(self):
        return server.make_app()

    def test_index_rout(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body.decode('utf-8'), 'Ready to fetch events')

    def test_one_event_json_handler(self):
        json_body = {
            'user': 'test_user',
            'events': [
                'test_event'
            ],
            'game': 'test_game'
        }
        json_response = {
            'event_status': 'accepted'
        }
        response = self.fetch('/', method='POST', body=json.dumps(json_body))
        self.assertEqual(json_response, json.loads(response.body)['data'])

    def test_wrong_event_args(self):
        json_body = {
            'user_wrong': 'test_user',
            'event_wrong': 'test_event',
            'game_wrong': 'test_game'
        }
        response = self.fetch('/', method='POST', body=json.dumps(json_body))
        self.assertEqual(response.code, 400)