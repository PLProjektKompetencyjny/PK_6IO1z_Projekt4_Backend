from flask import request, Blueprint, send_file, Response
from flask import current_app as app
from pathlib import Path

from http import HTTPStatus

from src.service.invoice_generator.invoice import InvoiceGenerator

invoice_controller = Blueprint('invoice_controller', __name__, url_prefix='/invoice')

@invoice_controller.route('/generate', methods=['GET'])
def generate():
    if request.method != 'GET':
        app.logger.error('Incorrect request method. This endpoint only accepts GET')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    reservation_id = request.args.get('reservation_id', type=int)
    tax_value = request.args.get('tax', type=int, default=8)

    if tax_value < 0:
        app.logger.error(f'Value of tax must be greater or equal 0. Value passed {tax_value}')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST

    if reservation_id is None or reservation_id <=0:
        app.logger.error(f'Value of reservation id must be greater than 0. Value passed {reservation_id}')
        return HTTPStatus.BAD_REQUEST.phrase, HTTPStatus.BAD_REQUEST


    invoice_generator_object = InvoiceGenerator(reservation_id, tax_value)
    invoice_file_path = invoice_generator_object.generate()

    try:
        with open(invoice_file_path, 'rb') as invoice_file:
                invoice_response = Response(invoice_file.read(), content_type='application/pdf')
                invoice_response.headers['Content-Disposition'] = f'filename={Path(invoice_file_path).stem}.pdf'
    except FileNotFoundError:
        app.logger.error(f'File with path: {invoice_file_path} could not be found')

    app.logger.info(f'Invoice for reservation {reservation_id} generated successfully')
    return invoice_response
