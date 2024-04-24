from abc import ABC
from logging import getLogger

from src.model.views.customer_view import CustomerView
from src.controller.views.view_controller import ViewController


class CustomerViewController(ViewController, ABC):
    def get(self):
        return self.get_rows(CustomerView, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
