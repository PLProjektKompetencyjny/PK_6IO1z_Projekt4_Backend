from os import getenv
from sys import argv

from unittest import TestLoader, TextTestRunner

from src import create_app

app = create_app(getenv('ENVIRONMENT') or 'dev')
app.app_context().push()


def run():
    app.run()


def test():
    tests = TestLoader().discover('./test', pattern='test*.py')
    result = TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    if len(argv) > 1 and argv[1] == 'run':
        run()
    else:
        test()
