from os import path, getcwd
from sys import path as sys_path

from flask_testing import TestCase

from src import create_app

PROJECT_PATH = getcwd()
SOURCE_PATH = path.join(PROJECT_PATH, "src")

sys_path.append(SOURCE_PATH)


class BaseTestCase(TestCase):
    def create_app(self):
        self.app = create_app('test')
        return self.app
