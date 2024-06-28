from abc import ABC
from logging import getLogger

from src.model.views.invoice_view import InvoiceView
from src.controller.views.view_controller import ViewController


class InvoiceViewController(ViewController, ABC):
    def get(self):
        return self.get_rows(InvoiceView, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
