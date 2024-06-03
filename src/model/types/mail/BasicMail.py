from abc import abstractmethod, ABCMeta
from os import getenv


class BasicMail(object, metaclass=ABCMeta):
    def __init__(self, data_id, recipients):
        self.message = None
        self.html_path = None
        self.recipients = recipients
        self.dataID = data_id
        self.logo_path = getenv('LOGO_HTTPS_PATH')
        self.__email = getenv('EMAIL_ADDRESS')

        if self.__email is None:
            raise ValueError

    def get_email(self):
        return self.__email

    @abstractmethod
    def create_message(self):
        pass
