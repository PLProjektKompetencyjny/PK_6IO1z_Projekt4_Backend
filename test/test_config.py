from flask import current_app
from flask_testing import TestCase

from unittest import main

from manage import app
from src.config import config_by_name


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object(config_by_name['dev'])
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['SECRET_KEY'] is 'my_precious_secret_key')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object(config_by_name['test'])
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['SECRET_KEY'] is 'my_precious_secret_key')
        self.assertTrue(app.config['DEBUG'] is True)


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object(config_by_name['prod'])
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    main()
