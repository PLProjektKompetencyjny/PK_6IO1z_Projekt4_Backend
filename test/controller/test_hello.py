from flask_testing import TestCase

from unittest import main

from manage import app
from src.config import config_by_name


class TestHello(TestCase):
    def create_app(self):
        app.config.from_object(config_by_name['test'])
        return app

    def test_hello_world(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!\n')


if __name__ == '__main__':
    main()
