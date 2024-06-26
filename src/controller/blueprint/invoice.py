from logging import getLogger
from flask import request, Blueprint, send_file, make_response
from flask import current_app as app

from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError

from src.controller.blueprint.auth import decode_access_token
from src.model.types.invoice.InvoiceGenerator import InvoiceGenerator
from src.model.views.reservation_view import ReservationView
from src.service.invoice_generator.invoice import generate
from src.controller.types.response import Response
from src.utils.utils import sqlalchemy_error_to_dict

logger = getLogger(__name__)

invoice = Blueprint('invoice_controller', __name__, url_prefix='/api')

def generate_invoice():
    if request.method != 'GET':
        app.logger.error('Incorrect request method. This endpoint only accepts GET')
        return Response.create(HTTPStatus.BAD_REQUEST, HTTPStatus.BAD_REQUEST.phrase, 'Incorrect method. Only GET is acceptable')



    reservation_id = request.args.get('reservation_id', type=int)
    tax_value = request.args.get('tax', type=int, default=8)

    if tax_value < 0:
        logger.error(f'Value of tax must be greater or equal 0. Value passed {tax_value}')
        return Response.create(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,f'Value of tax must be greater or equal 0. Value passed {tax_value}')

    if reservation_id is None or reservation_id <=0:
        logger.error(f'Value of reservation id must be greater than 0. Value passed {reservation_id}')
        return Response.create(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,f'Value of reservation id must be greater than 0. Value passed {reservation_id}')


    data = decode_access_token()
    client_id_reservation = ReservationView.get_customer_id_from_reservation_id(reservation_id, logger)
    if client_id_reservation == None:
        logger.error(f'No such reservation id: {reservation_id}')
        return Response.create(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase)

    if(client_id_reservation[0] != data['user_id'] and data['user_is_admin'] != True):
        logger.error(f'Insufficient privileges for this operation')
        return Response.create(HTTPStatus.FORBIDDEN,HTTPStatus.FORBIDDEN.phrase)
    try:
        invoice_generator_object = InvoiceGenerator(reservation_id, tax_value)
        invoice_file_path = generate(invoice_generator_object)
    except SQLAlchemyError as e:
        error_details = sqlalchemy_error_to_dict(e)
        app.logger.error(f'Problem with data  base occured: {error_details}')
        return Response.create(HTTPStatus.BAD_REQUEST, error_details)
    except FileNotFoundError:
        logger.error(f'Problem with file occured')
        return Response.create(HTTPStatus.INTERNAL_SERVER_ERROR, 'File not found for the method')


    response = make_response(send_file(invoice_file_path, as_attachment=True, mimetype='application/pdf'))
    response.status_code = HTTPStatus.OK
    logger.info(f'Invoice for reservation {reservation_id} generated successfully')
    return response

invoice.add_url_rule('/invoice/generate', view_func=generate_invoice, methods=['GET'])

