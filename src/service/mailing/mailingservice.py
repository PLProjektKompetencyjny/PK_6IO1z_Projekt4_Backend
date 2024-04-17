import smtplib
from os import getenv
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from abc import  abstractmethod, ABCMeta


class BasicMail(object, metaclass=ABCMeta):
    def __init__(self, data_id, recipients):
        self.message = None
        self.html_path = None
        self.recipients = recipients
        self.dataID = data_id
        self.logo_path = getenv('LOGO_HTTPS_PATH')
        self.__email = getenv('EMAIL_ADDRESS')

    def get_email(self):
        return self.__email

    @abstractmethod
    def create_message(self):
        pass


class ActivationMessageMail(BasicMail):

    def __init__(self, data_id, recipients):
        super().__init__(data_id, recipients)
        self.html_path = 'src/templates/HTML_EMAIL/account-confirmation.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{url_path}', 'onet.pl')

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = f'Activate your account'
        self.message['From'] = self.get_email()
        self.message['To'] = ', '.join(self.recipients)
        return self.message

class ResetPasswordMessageMail(BasicMail):
    def __init__(self, data_id, recipients):
        super().__init__(data_id, recipients)
        self.html_path = 'src/templates/HTML_EMAIL/password.html'

    def create_message(self):

        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reset_password}', 'onet.pl')

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = 'Reset password'
        self.message['From'] = self.get_email()
        self.message['To'] = ', '.join(self.recipients)
        return self.message

class ReservationConfirmationMessageMail(BasicMail):
    def __init__(self, data_id, recipients):
        super().__init__(data_id, recipients)
        self.html_path = 'src/templates/HTML_EMAIL/reservation-confirmation.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reservation_id}', str(self.dataID))

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = f'Reservation with ID {self.dataID} confirmed!'
        self.message['From'] = self.get_email()
        self.message['To'] = ', '.join(self.recipients)
        return self.message

class InvoiceMessageMail(BasicMail):
    def __init__(self, data_id, recipients):
        super().__init__(data_id, recipients)
        self.html_path = 'src/templates/HTML_EMAIL/invoice.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reservation_id}', str(self.dataID))

        self.message = MIMEMultipart()
        html_message_body = MIMEText(html_message, 'html')

        self.message.attach(html_message_body)
        with open('src/templates/HTML_EMAIL/images/Minutka_symulacjaRadia.pdf', "rb") as file:
            attachment = MIMEApplication(file.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename='Minutka_symulacjaRadia')
        self.message.attach(attachment)

        self.message['Subject'] = f'Your invoice for reservation {self.dataID} landed.'
        self.message['From'] = self.get_email()
        self.message['To'] = ', '.join(self.recipients)
        return self.message

class PaymentConfirmationMessageMail(BasicMail):
    def __init__(self, data_id, recipients):
        super().__init__(data_id, recipients)
        self.html_path = 'src/templates/HTML_EMAIL/payment.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reservation_id}', str(self.dataID))

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = f'Payment for reservation {self.dataID} accepted!'
        self.message['From'] = self.get_email()
        self.message['To'] = ', '.join(self.recipients)
        return self.message


class MailingService:
    def __init__(self):
        self.__EMAIL = getenv('EMAIL_ADDRESS')
        self.__PASSWORD = getenv('EMAIL_PASS')
    def send_email(self, message, recipients):
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
               smtp_server.login(self.__EMAIL, self.__PASSWORD)
               smtp_server.sendmail(self.__EMAIL, recipients, message.as_string())

