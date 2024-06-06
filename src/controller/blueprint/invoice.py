from flask import request, Blueprint, send_file, make_response
from flask import current_app as app

from http import HTTPStatus

from src.model.types.invoice.InvoiceGenerator import InvoiceGenerator
from src.service.invoice_generator.invoice import generate
from src.controller.types.response import Response

invoice = Blueprint('invoice_controller', __name__, url_prefix='/api')

def generate_invoice():
    if request.method != 'GET':
        app.logger.error('Incorrect request method. This endpoint only accepts GET')
        return Response.create(HTTPStatus.BAD_REQUEST, HTTPStatus.BAD_REQUEST.phrase, 'Incorrect method. Only GET is acceptable')

    reservation_id = request.args.get('reservation_id', type=int)
    tax_value = request.args.get('tax', type=int, default=8)

    if tax_value < 0:
        app.logger.error(f'Value of tax must be greater or equal 0. Value passed {tax_value}')
        return Response.create(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,f'Value of tax must be greater or equal 0. Value passed {tax_value}')

    if reservation_id is None or reservation_id <=0:
        app.logger.error(f'Value of reservation id must be greater than 0. Value passed {reservation_id}')
        return Response.create(HTTPStatus.BAD_REQUEST,HTTPStatus.BAD_REQUEST.phrase,f'Value of reservation id must be greater than 0. Value passed {reservation_id}')


    invoice_generator_object = InvoiceGenerator(reservation_id, tax_value)
    invoice_file_path = generate(invoice_generator_object)

    response = make_response(send_file(invoice_file_path, as_attachment=True, mimetype='application/pdf'))
    response.status_code = HTTPStatus.OK


    app.logger.info(f'Invoice for reservation {reservation_id} generated successfully')
    return response

invoice.add_url_rule('/invoice/generate', view_func=generate_invoice, methods=['GET'])

