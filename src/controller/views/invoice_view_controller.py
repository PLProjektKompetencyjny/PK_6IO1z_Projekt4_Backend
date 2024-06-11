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

        self.logger.info(f"New request with params: {params}")

        result = InvoiceView.add_invoice(
            **params
        )

        return result

    def put(self):
        pass

    def delete(self):
        pass
