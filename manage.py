from os import getenv
from sys import argv

from unittest import TestLoader, TextTestRunner

from src import create_app


class Manager:
    def __init__(self):
        self.app = create_app(getenv('ENVIRONMENT') or 'dev')

    def run(self):
        self.app.app_context().push()
        self.app.run(threaded=True)

    @staticmethod
    def test():
        tests = TestLoader().discover('./test', pattern='test*.py')
        result = TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            return 0
        return 1


if __name__ == '__main__':
    if len(argv) < 1 or len(argv) > 2:
        print("Bad arguments")
        exit(1)

    manager = Manager()

    if argv[1] == 'run':
        manager.run()

    if argv[1] == 'test':
        manager.test()
