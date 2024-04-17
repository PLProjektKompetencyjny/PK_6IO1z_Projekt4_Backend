from flask import request, Blueprint
from flask import current_app as app

from smtplib import SMTPResponseException
from http import HTTPStatus

from src.service.mailing.mailingservice import (ReservationConfirmationMessageMail, InvoiceMessageMail,
                                                ResetPasswordMessageMail, PaymentConfirmationMessageMail,
                                                ActivationMessageMail, MailingService, MissingPassword, MissingEmailAddress)

mailing = Blueprint('mailing', __name__, url_prefix='/mailing')

def SelectMessageCreator(message_type, data_id, recipients):
    if message_type == 1:
        return ActivationMessageMail(data_id, recipients).create_message()

    if message_type == 2:
        return ResetPasswordMessageMail(data_id, recipients).create_message()

    if message_type == 3:
      return ReservationConfirmationMessageMail(data_id, recipients).create_message()

    if message_type == 4:
      return InvoiceMessageMail(data_id, recipients).create_message()

    if message_type == 5:
        return PaymentConfirmationMessageMail(data_id, recipients).create_message()

@mailing.route('/sendmail', methods=['GET'])
def sendmail():
    data_id = request.args.get('data_id', type=int)
    address = request.args.get('address', type=str, default='')
    message_type = request.args.get('message_type', type=int)

    if data_id < 0:
        app.logger.warning(f'data_id must be greater than 0. Passed Value: {data_id}')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    if not address or address.find('@') == -1:
        app.logger.warning(f'Check email address passed in request. Passed Value: {address}')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    if message_type not in range(1,6):
        app.logger.warning(f'Invalid message type passed to method. Passed Value: {message_type}')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    recipients = address.split(',')

    try:
        message = SelectMessageCreator(message_type, data_id, recipients)

    except ValueError as e:
        app.logger.error(f'''Problem occurred during message generation: {str(e)}.
                             passed data: data_id: {data_id}, address: {address}, message_type: {message_type}''')
        return HTTPStatus.INTERNAL_SERVER_ERROR.phrase, HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        app.logger.info(f'Message created with id of data: {data_id} and type: {message_type}')


    try:
        MailingService().send_email(message, recipients)

    except SMTPResponseException as e:
        error_code = e.smtp_code
        error_message = e.smtp_error
        app.logger.error(f'Error with sending email with SMTP. Code: {error_code}. Message: {error_message}')
        return HTTPStatus.SERVICE_UNAVAILABLE.phrase, HTTPStatus.SERVICE_UNAVAILABLE

    except ValueError as e:
        app.logger.error(f'Value error: {str(e)}')
        return HTTPStatus.INTERNAL_SERVER_ERROR.phrase, HTTPStatus.INTERNAL_SERVER_ERROR

    except MissingPassword:
        app.logger.error(f'Password for mail account is missing. Check .env file for details')
        return HTTPStatus.INTERNAL_SERVER_ERROR.phrase, HTTPStatus.INTERNAL_SERVER_ERROR

    except MissingEmailAddress:
        app.logger.error(f'Email address for mail account is missing. Check .env file for details')
        return HTTPStatus.INTERNAL_SERVER_ERROR.phrase, HTTPStatus.INTERNAL_SERVER_ERROR

    else:
        app.logger.info(f'Mail to {recipients} with message type {message_type} has been sent successfully.')

    return HTTPStatus.OK.phrase, HTTPStatus.OK