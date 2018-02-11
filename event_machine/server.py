import json

import tornado.ioloop
import tornado.web
from tornado_json import schema
from tornado_json.requesthandlers import APIHandler

USER_INPUT = {
    'title': 'event',
    'type': 'object',
    'description': 'A event from authenticated user in game',
    'properties': {
        'user': {
            'description': 'user name',
            'type': 'string'
        },
        'events': {
            'description': 'list of events in game',
            'type': 'array',
            'items': {'type': 'string'},
            'minItems': 1
        }
    },
    'required': ['user', 'events', 'game']
}

OUTPUT_EVENT = {
    'title': 'event_status',
    'type': 'object',
    'description': 'A status that got from the event'
                   ' registered authenticated user in game',
    'properties': {
        'event_status': {
            'description': 'status of the event',
            'type': 'string'
        },
    },
    'required': ['event_status']
}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Ready to fetch events')


class EventHandler(APIHandler):
    @schema.validate(input_schema=USER_INPUT, output_schema=OUTPUT_EVENT)
    def post(self):
        """Event Trigger via authenticated user in game"""
        user_event = json.loads(self.request.body)
        # TODO implement logic
        return {'event_status': 'accepted'}


def make_app():
    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/events', EventHandler),
    ])


if __name__ == '__main__':
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
