from flask import url_for

from test import BaseTestCase


class TestDatabase(BaseTestCase):
    def test_get_rooms(self):
        response = self.client.get(url_for('hello.get_rooms'))

        self.assert200(response)
        self.assertEqual(response.json, [])
