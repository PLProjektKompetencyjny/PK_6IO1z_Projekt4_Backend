from flask import Blueprint
from smtplib import SMTPResponseException

from src.service.mailing.mailservice import (CreateReservationConfirmationMessage, CreateInvoiceMessage,
                                             CreateResetPasswordMessage, CreatePaymentConfirmationMessage,
                                             CreateActivationMessage, MailService)

from manage import app
from src import mailing



@mailing.route('/sendmail/<int:data_id>/<string:address>/<int:message_type>', methods='POST')
def sendmail(data_id, address, message_type):
    if data_id < 0  or not address or message_type not in range(1,6):
        app.logger.warning(f'Invalid data passed to method')
        return 400

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
        app.logger.error(f'''Problem occurred during message generation: {str(e)}.
                             passed data: data_id: {data_id}, address: {address}, message_type: {message_type}''')
        return 500
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
        return 500
    finally:
        app.logger.info(f'Mail to {recipients} with message type {message_type} has been sent successfully.')
    return 200