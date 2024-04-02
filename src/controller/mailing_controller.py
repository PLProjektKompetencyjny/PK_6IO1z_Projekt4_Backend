from smtplib import SMTPResponseException
from flask import request, Blueprint
from flask import current_app as app
from http import HTTPStatus

from src.service.mailing.mailservice import (CreateReservationConfirmationMessage, CreateInvoiceMessage,
                                             CreateResetPasswordMessage, CreatePaymentConfirmationMessage,
                                             CreateActivationMessage, MailService)

mailing = Blueprint('mailing', __name__, url_prefix='/mailing')

def SelectMessageCreator(message_type, data_id, recipients):
    if message_type == 1:
        return CreateActivationMessage(data_id, recipients).create_message()

    if message_type == 2:
        return CreateResetPasswordMessage(data_id, recipients).create_message()

    if message_type == 3:
      return CreateReservationConfirmationMessage(data_id, recipients).create_message()

    if message_type == 4:
      return CreateInvoiceMessage(data_id, recipients).create_message()

    if message_type == 5:
        return CreatePaymentConfirmationMessage(data_id, recipients).create_message()

@mailing.route('/sendmail', methods=['POST'])
def sendmail():
    data_id = request.args.get('data_id', type=int)
    address = request.args.get('address', type=str, default='')
    message_type = request.args.get('message_type', type=int)

    if data_id < 0  or not address or message_type not in range(1,6):
        app.logger.warning(f'Invalid data passed to method')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    recipients = address.split(',')

    try:
        message = SelectMessageCreator(message_type, data_id, recipients)
    except ValueError as e:
        app.logger.error(f'''Problem occurred during message generation: {str(e)}.
                             passed data: data_id: {data_id}, address: {address}, message_type: {message_type}''')
        return HTTPStatus.INTERNAL_SERVER_ERROR.phrase, HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        app.logger.info(f'Message created with id of data: {data_id} and type: {message_type}')

    try:
        MailService().send_email(message, recipients)
    except SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        app.logger.error(f'Error with sending email with SMTP. Code: {error_code}. Message: {error_message}')
        return 503
    except ValueError as e:
        app.logger.error(f'Value error: {str(e)}')
        return HTTPStatus.INTERNAL_SERVER_ERROR.phrase, HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        app.logger.info(f'Mail to {recipients} with message type {message_type} has been sent successfully.')
    return HTTPStatus.OK.phrase, HTTPStatus.OK