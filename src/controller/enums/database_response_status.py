from enum import Enum


class DatabaseResponseStatus(Enum):
    # dodaj więcej kodów błędów, opisz je bardziej szczegółowo
    OK = 0, 'OK'
    DATABASE_ERROR = 1, 'Database error'
    NOT_FOUND = 2, 'No rows found'

    def get_status(self):
        return self.name, self.value[0]

    def get_value(self):
        return self.value[0]

    def get_description(self):
        return self.value[1]
