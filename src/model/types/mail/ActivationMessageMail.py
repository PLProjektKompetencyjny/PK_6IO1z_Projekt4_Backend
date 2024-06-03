from email.mime.text import MIMEText

from src.model.types.mail.BasicMail import BasicMail


class ActivationMessageMail(BasicMail):

    def __init__(self, data_id, recipients):
        super().__init__(data_id, recipients)
        self.html_path = 'src/model/templates/HTML_EMAIL/account-confirmation.html'

    def create_message(self):
        html_message = open(self.html_path).read()
        html_message = html_message.replace('{logo_path}', self.logo_path).replace('{url_path}', 'onet.pl')

        self.message = MIMEText(html_message, 'html')
        self.message['Subject'] = f'Activate your account'
        self.message['From'] = self.get_email()
        self.message['To'] = ', '.join(self.recipients)
        return self.message
