from logging import getLogger

import sqlalchemy
from flask import request, Blueprint, send_file, make_response
from flask import current_app as app
from flask_jwt_extended import jwt_required

from http import HTTPStatus

from sqlalchemy.exc import SQLAlchemyError

from src.controller.blueprint.auth import decode_access_token
from src.model.types.invoice.InvoiceGenerator import InvoiceGenerator
from src.model.views.reservation_view import ReservationView
from src.service.invoice_generator.invoice import generate
from src.controller.types.response import Response
from src.utils.utils import sqlalchemy_error_to_dict

#API invoice

#API for invoice is under URL /api/invoice

logger = getLogger(__name__)

invoice = Blueprint('invoice_controller', __name__, url_prefix='/api')

#Endpoint generate_invoice takes two positional arguments which are:
#reservation_id:int - number of reservation for which invoice has to be generated. It has to be greater than 0.
#tax:int - value of the tax for the invoice, by default it is 8. It has to be between (0;100>.
#returns content of the generated file in the body of response. The type of response is application/pdf.
def generate_invoice():
    if request.method != 'GET':
        app.logger.error('Incorrect request method. This endpoint only accepts GET')
        return Response.create(HTTPStatus.BAD_REQUEST, HTTPStatus.BAD_REQUEST.phrase, 'Incorrect method. Only GET is acceptable')



    reservation_id = request.args.get('reservation_id', type=int)
    tax_value = request.args.get('tax', type=int, default=8)

    if tax_value < 0 or tax_value > 100:
        logger.error(f'Value of tax must fit in range (0;100>. Value passed {tax_value}')
        return Response.create(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,f'Value of tax must fit in range (0;100>. Value passed {tax_value}')

    if reservation_id is None or reservation_id <=0:
        logger.error(f'Value of reservation id must be greater than 0. Value passed {reservation_id}')
        return Response.create(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,f'Value of reservation id must be greater than 0. Value passed {reservation_id}')


    data = decode_access_token()
    if data is None:
        logger.error(f'No token passed to endpoint. It is required to access this endpoint.')
        return Response.create(HTTPStatus.FORBIDDEN, HTTPStatus.FORBIDDEN.phrase,f'No token passed to endpoint. It is required to access this endpoint.')
    try:
        client_id_reservation = ReservationView.get_customer_id_from_reservation_id(reservation_id, logger)
    except sqlalchemy.orm.exc.NoResultFound:
        logger.error(f'No such reservation id: {reservation_id}')
        return Response.create(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, f'No such reservation id: {reservation_id}')


    if client_id_reservation != data['user_id'] and data['user_is_admin'] != True:
        logger.error(f'Insufficient privileges for this operation')
        return Response.create(HTTPStatus.FORBIDDEN,HTTPStatus.FORBIDDEN.phrase, f'Insufficient privileges for this operation')
    try:
        invoice_generator_object = InvoiceGenerator(reservation_id, tax_value)
        invoice_file_path = generate(invoice_generator_object)
    except SQLAlchemyError as e:
        error_details = sqlalchemy_error_to_dict(e)
        app.logger.error(f'Problem with data  base occured: {error_details}')
        return Response.create(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, error_details)
    except FileNotFoundError:
        logger.error(f'Problem with file occured')
        return Response.create(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR, 'File not found for the method')
    except sqlalchemy.orm.exc.NoResultFound:
        logger.error(f'There is no records of data with given reservation id: {reservation_id}')
        return Response.create(HTTPStatus.INTERNAL_SERVER_ERROR, HTTPStatus.INTERNAL_SERVER_ERROR.phrase, f'There is no records of data with given reservation id: {reservation_id}')



    response = make_response(send_file(invoice_file_path, as_attachment=True, mimetype='application/pdf'))
    response.status_code = HTTPStatus.OK
    logger.info(f'Invoice for reservation {reservation_id} generated successfully')
    return response


invoice.add_url_rule('/invoice/generate', view_func=generate_invoice, methods=['GET'])

