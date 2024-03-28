from flask import Blueprint
from smtplib import SMTPResponseException, SMTPException

from src.service.mailing.mailservice import CreateReservationConfirmationMessage, CreateInvoiceMessage, CreateResetPasswordMessage, CreatePaymentConfirmationMessage, CreateActivationMessage, MailService
from manage import app

mailing = Blueprint('mailing', __name__)

@mailing.route('/send-mail/<int:data_id>/<string:address/<int:message_type>')
def send_mail(data_id, address, message_type):
    if data_id is None or address is None or message_type is None or message_type not in range(1,6):
        return 406

    recipients = address.split(',')
    message = None
    try:
        if message_type == 1:
            message = CreateActivationMessage(data_id, recipients).create_message()
        elif message_type == 2:
            message = CreateResetPasswordMessage(data_id, recipients).create_message()
        elif message_type == 3:
            message = CreateReservationConfirmationMessage(data_id, recipients).create_message()
        elif message_type == 4:
            message = CreateInvoiceMessage(data_id, recipients).create_message()
        elif message_type == 5:
            message = CreatePaymentConfirmationMessage(data_id, recipients).create_message()
    except ValueError as e:
        app.logger.error(f'Problem occurred when generating message: {e}')
    finally:
        app.logger.info(f'Message created with id: {data_id} and type: {message_type}')

    if message is None:
        app.logger.warning('Incorrect value passed to method. Message type has to be between 1 and 5!')
        return 406

    try:
        MailService().send_email(message, recipients)
    except SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        app.logger.error(f'Error with sending email with SMTP. Code: {error_code}. Message: {error_message}')
    except ValueError as e:
        app.logger.error(f'Value error: {e}')
    finally:
        app.logger.info(f'Mail to {recipients} has been sent successfully.')
    return 204