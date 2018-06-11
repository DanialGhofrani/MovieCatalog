from unittest import TestCase
from server.models import Movie, Actor, MovieActor
import json
import wsgi


class ModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """
            create all database tables if necessary and wipe them
        """
        super(ModelTestCase, cls).setUpClass()
        if not Movie.table_exists():
            Movie.create_table()
        if not Actor.table_exists():
            Actor.create_table()
        if not MovieActor.table_exists():
            MovieActor.create_table()

    def setUp(self):
        """
            delete all records before running test
        """
        MovieActor.delete().execute()
        Movie.delete().execute()
        Actor.delete().execute()


class EndpointTestCase(ModelTestCase):
    def setUp(self):
        super(EndpointTestCase, self).setUp()
        self.test_client = wsgi.app.test_client()

    def post_json(self, endpoint, payload, headers=None):
        length = len(json.dumps(payload))
        default_headers = {
            'Content-Type': 'application/json',
            'Content-Length': length,
        }
        if headers is not None:
            default_headers.update(headers)
        res = self.test_client.post(endpoint, headers=default_headers, data=json.dumps(payload))
        return res
