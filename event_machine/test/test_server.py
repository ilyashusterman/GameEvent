import json

import os
from tornado.testing import AsyncHTTPTestCase

from event_machine import server

INDEX_HTML_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                               'index.html'))


class TestServer(AsyncHTTPTestCase):
    def get_app(self):
        return server.make_app()

    def test_index_rout(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        with open(INDEX_HTML_PATH, 'r') as f:
            content = f.read()

            self.assertEqual(response.body.decode('utf-8'), content)

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
        response = self.fetch('/events', method='POST',
                              body=json.dumps(json_body))
        self.assertEqual(json_response, json.loads(response.body)['data'])

    def test_wrong_event_args(self):
        json_body = {
            'user_wrong': 'test_user',
            'event_wrong': 'test_event',
            'game_wrong': 'test_game'
        }
        response = self.fetch('/events', method='POST',
                              body=json.dumps(json_body))
        self.assertEqual(response.code, 400)

    def test_save_events(self):
        pass
