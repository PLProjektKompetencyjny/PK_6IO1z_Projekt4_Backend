import smtplib
from os import getenv


class MissingEmailAddress(Exception):
    pass


class MissingPassword(Exception):
    pass


class MailingService:
    def __init__(self):
        self.__email = getenv('EMAIL_ADDRESS')
        self.__password = getenv('EMAIL_PASS')

        if self.__email is None:
            raise MissingEmailAddress
        if self.__password is None:
            raise MissingPassword

    def send_email(self, message, recipients):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(self.__email, self.__password)
            smtp_server.sendmail(self.__email, recipients, message.as_string())
