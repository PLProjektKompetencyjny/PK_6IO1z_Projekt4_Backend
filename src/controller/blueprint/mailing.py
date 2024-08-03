from re import match

from flask import request, Blueprint
from flask import current_app as app

from smtplib import SMTPResponseException
from http import HTTPStatus

from src.model.types.mail.ActivationMessageMail import ActivationMessageMail
from src.model.types.mail.InvoiceMessageMail import InvoiceMessageMail
from src.model.types.mail.PaymentConfirmationMessageMail import PaymentConfirmationMessageMail
from src.model.types.mail.ResetPasswordMessageMail import ResetPasswordMessageMail
from src.model.types.mail.ReservationConfirmationMessageMail import ReservationConfirmationMessageMail
from src.service.mailing.mailingservice import MailingService, MissingPassword, MissingEmailAddress

mailing = Blueprint('mailing', __name__, url_prefix='/api')


def SelectMessageCreator(message_type, data_id, recipients):
    mail_types = {
        'Activation': ActivationMessageMail,
        'Invoice': InvoiceMessageMail,
        'Payment': PaymentConfirmationMessageMail,
        'Reservation': ReservationConfirmationMessageMail,
        'ResetPassword': ResetPasswordMessageMail
    }

    return mail_types[message_type](data_id=data_id, recipients=recipients)


def CheckEMailAddress(address: str):
    if not address:
        return False

    regex = r'^[A-Za-z0-9]+[.-_]*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+$'

    if match(regex, address):
        return True

    return False


def CheckDataId(data_id: str):
    if not data_id:
        return False

    return int(data_id) > 0


def sendmail():
    if request.method != 'POST':
        app.logger.warning(f'This endpoint supports only POST operation')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    data_id = request.args.get('data_id')
    address = request.args.get('address', type=str, default='')
    message_type = request.args.get('message_type', type=str)

    if CheckDataId(data_id) is False:
        app.logger.warning(f'data_id must be greater than 0. Passed Value: {data_id}')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    if CheckEMailAddress(address) is False:
        app.logger.warning(f'Check email address passed in request. Passed Value: {address}')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    recipients = address.split(',')

    try:
        message = SelectMessageCreator(message_type, data_id, recipients).create_message()
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


mailing.add_url_rule('mailing/sendmail', view_func=sendmail, methods=['POST'])
