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


def sendmail():
    data_id = request.args.get('data_id', type=int)
    address = request.args.get('address', type=str, default='')
    message_type = request.args.get('message_type', type=str)

    if data_id < 0:
        app.logger.warning(f'data_id must be greater than 0. Passed Value: {data_id}')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    if not address or address.find('@') == -1:
        app.logger.warning(f'Check email address passed in request. Passed Value: {address}')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    recipients = address.split(',')

    try:
        messageCreator = SelectMessageCreator(message_type, data_id, recipients)
        message = messageCreator.create_message()
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
