import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from os import getenv
from abc import ABC, abstractmethod

load_dotenv()
EMAIL = getenv('EMAIL_ADDRESS')
PASSWORD = getenv('EMAIL_PASS')
LOGO_PATH = getenv('LOGO_HTTPS_PATH')

class CreateMail(ABC):
    def __init__(self, dataID):
        self.message = None
        self.recipients = ['sobonukasz@gmail.com']
        self.dataID = dataID
        self.logo_path = LOGO_PATH

    @abstractmethod
    def create_message(self):
        pass

class CreateResetPasswordMessage(CreateMail):
    def __init__(self, dataID):
        super().__init__(dataID)
        self.html_path = '../../templates/HTML_EMAIL/password.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reset_password}', 'onet.pl')

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = 'Reset password'
        self.message['From'] = EMAIL
        self.message['To'] = ', '.join(self.recipients)
        return self.message

class CreateReservationConfirmationMessage(CreateMail):
    def __init__(self, dataID):
        super().__init__(dataID)
        self.html_path = '../../templates/HTML_EMAIL/reservation-confirmation.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reservation_id}', str(self.dataID))

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = f'Reservation with ID {self.dataID} confirmed!'
        self.message['From'] = EMAIL
        self.message['To'] = ', '.join(self.recipients)
        return self.message

class CreateInvoiceMessage(CreateMail):
    def __init__(self, dataID):
        super().__init__(dataID)
        self.html_path = '../../templates/HTML_EMAIL/invoice.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reservation_id}', str(self.dataID))

        self.message = MIMEMultipart()
        htmlMessageBody = MIMEText(html_message, 'html')

        self.message.attach(htmlMessageBody)
        with open('../../templates/HTML_EMAIL/images/Minutka_symulacjaRadia.pdf', "rb") as file:
            attachment = MIMEApplication(file.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename='Minutka_symulacjaRadia')
        self.message.attach(attachment)

        self.message['Subject'] = f'Your invoice for reservation {self.dataID} landed.'
        self.message['From'] = EMAIL
        self.message['To'] = ', '.join(self.recipients)
        return self.message

class CreatePaymentConfirmationMessage(CreateMail):
    def __init__(self, dataID):
        super().__init__(dataID)
        self.html_path = '../../templates/HTML_EMAIL/payment.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reservation_id}', str(self.dataID))

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = f'Payment for reservation {self.dataID} accepted!'
        self.message['From'] = EMAIL
        self.message['To'] = ', '.join(self.recipients)
        return self.message

class CreateActivationMessage(CreateMail):
    def __init__(self, dataID):
        super().__init__(dataID)
        self.html_path = '../../templates/HTML_EMAIL/account-confirmation.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{url_path}', 'onet.pl')

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = f'Activate your account'
        self.message['From'] = EMAIL
        self.message['To'] = ', '.join(self.recipients)
        return self.message
class Mailing:
    def send_email(self, message, recipients):
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
           smtp_server.login(EMAIL, PASSWORD)
           smtp_server.sendmail(EMAIL, recipients, message.as_string())
        print("Message sent!")

mailingObj = Mailing()
messageObj = CreateActivationMessage(100)
message = messageObj.create_message()
mailingObj.send_email(message, messageObj.recipients)
