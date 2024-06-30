from abc import ABC
from logging import getLogger

from flask import request

from src.model.views.invoice_view import InvoiceView
from src.controller.views.view_controller import ViewController

from src.utils.utils import getViewFields

class InvoiceViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        return self.get_rows(InvoiceView, getLogger(__name__))

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
        params = {}
        for key in getViewFields(InvoiceView, excluded_columns):
            params[key] = request.form.get(key, None)

        self.logger.info(f"New POST request with params: {params}")

        return InvoiceView.add_invoice(
            **params
        )

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
        params = {}
        for key in getViewFields(InvoiceView, excluded_columns):
            params[key] = request.form.get(key, None)

        self.logger.info(f"New PUT request with params: {params}")

        return InvoiceView.update_invoice(
            **params
        )

    def delete(self):
        pass
