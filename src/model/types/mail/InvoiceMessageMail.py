from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.model.types.mail.BasicMail import BasicMail


class InvoiceMessageMail(BasicMail):
    def __init__(self, data_id, recipients):
        super().__init__(data_id, recipients)
        self.html_path = 'src/model/templates/HTML_EMAIL/invoice.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reservation_id}', str(self.dataID))

        self.message = MIMEMultipart()
        html_message_body = MIMEText(html_message, 'html')

        self.message.attach(html_message_body)
        '''
        with open('src/templates/HTML_EMAIL/images/Minutka_symulacjaRadia.pdf', "rb") as file:
            attachment = MIMEApplication(file.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename='Minutka_symulacjaRadia')
        self.message.attach(attachment)
        '''
        self.message['Subject'] = f'Your invoice for reservation {self.dataID} landed.'
        self.message['From'] = self.get_email()
        self.message['To'] = ', '.join(self.recipients)
        return self.message
