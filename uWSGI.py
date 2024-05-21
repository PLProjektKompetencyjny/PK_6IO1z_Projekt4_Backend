import os
from src import create_app
from manage import Manager

app = create_app(os.getenv('ENVIRONMENT', 'prod'))
