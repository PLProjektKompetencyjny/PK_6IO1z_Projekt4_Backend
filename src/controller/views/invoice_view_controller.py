from abc import ABC
from logging import getLogger

from flask import request
from flask_jwt_extended import jwt_required

from src.model.views.invoice_view import InvoiceView
from src.controller.views.view_controller import ViewController
from src.service.payments.payments import get_payment_ids_to_check

from src.utils.utils import getViewFields, get_params



class InvoiceViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    @jwt_required()
    def get(self):
        payment_ids_check = request.args.get('get_payment_ids_to_check', type=bool, default=False)

        if payment_ids_check:
            return get_payment_ids_to_check()

        return self.get_rows(InvoiceView, getLogger(__name__))

    @jwt_required()
    def post(self):
        excluded_columns = [
            'invoice_id',
            'invoice_room_id',
            'invoice_room_price_gross',
            'invoice_date',
            'invoice_price_gross',
            'invoice_is_paid',
            'invoice_status_id',
            'invoice_last_modified_by',
            'invoice_last_modified_at'
        ]
        params = get_params(request.form, InvoiceView, excluded_columns)

        self.logger.info(f"New POST request with params: {params}")

        return InvoiceView.add_invoice(
            **params
        )

    @jwt_required()
    def put(self):
        excluded_columns = [
            'invoice_room_id',
            'invoice_reservation_id',
            'invoice_room_price_gross',
            'invoice_date',
            'invoice_price_gross',
            'invoice_is_paid',
            'invoice_last_modified_by',
            'invoice_last_modified_at'
        ]
        params = get_params(request.form, InvoiceView, excluded_columns)

        self.logger.info(f"New PUT request with params: {params}")

        return InvoiceView.update_invoice(
            **params
        )

    def delete(self):
        pass
