from email.mime.text import MIMEText

from src.model.types.mail.BasicMail import BasicMail


class PaymentConfirmationMessageMail(BasicMail):
    def __init__(self, data_id, recipients):
        super().__init__(data_id, recipients)
        self.html_path = 'src/model/templates/HTML_EMAIL/payment.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{reservation_id}', str(self.dataID))

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = f'Payment for reservation {self.dataID} accepted!'
        self.message['From'] = self.get_email()
        self.message['To'] = ', '.join(self.recipients)
        return self.message
