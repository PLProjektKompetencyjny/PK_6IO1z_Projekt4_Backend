from unittest import main

from src import create_app
from test import BaseTestCase


class TestDevelopmentConfig(BaseTestCase):
    def create_app(self):
        self.app = create_app('dev')
        return self.app

    def test_app_is_development(self):
        self.assertFalse(self.app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(self.app.config['SECRET_KEY'] == 'my_precious_secret_key')
        self.assertTrue(self.app.config['DEBUG'] is True)
        self.assertFalse(self.app is None)


class TestTestingConfig(BaseTestCase):

    def test_app_is_testing(self):
        self.assertFalse(self.app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(self.app.config['SECRET_KEY'] == 'my_precious_secret_key')
        self.assertTrue(self.app.config['DEBUG'] is True)


class TestProductionConfig(BaseTestCase):
    def create_app(self):
        self.app = create_app('prod')
        return self.app

    def test_app_is_production(self):
        self.assertTrue(self.app.config['DEBUG'] is False)


if __name__ == '__main__':
    main()
