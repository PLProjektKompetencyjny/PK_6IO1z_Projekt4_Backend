from abc import ABC
from logging import getLogger

from flask import request

from src.model.views.invoice_view import InvoiceView
from src.controller.views.view_controller import ViewController


class InvoiceViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        return self.get_rows(InvoiceView, getLogger(__name__))

    def post(self):
        params = {
            "reservation_id": int(request.form['reservation_id']),
        }

        self.logger.info(f"New POST request with params: {params}")

        return InvoiceView.add_invoice(
            **params
        )

    def put(self):
        params = {
            "invoice_id": int(request.form['invoice_id']),
            "invoice_status_id": int(request.form['invoice_status_id']),
        }

        self.logger.info(f"New PUT request with params: {params}")

        return InvoiceView.update_invoice(
            **params
        )

    def delete(self):
        pass
