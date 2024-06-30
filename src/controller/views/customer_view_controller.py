from abc import ABC
from logging import getLogger
from flask import request

from src.model.views.customer_view import CustomerView
from src.controller.views.view_controller import ViewController

from src.utils.utils import getViewFields, get_params


class CustomerViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        return self.get_rows(CustomerView, getLogger(__name__))

    def post(self):
        excluded_columns = ['customer_last_modified_at', 'customer_id']
        params = get_params(request.form, CustomerView, excluded_columns)

        self.logger.info(f"New POST request with params: {params}")

        return CustomerView.add_customer(**params)

    def put(self):
        excluded_columns = ['customer_last_modified_at']
        params = get_params(request.form, CustomerView, excluded_columns)

        self.logger.info(f"New PUT request with params: {params}")

        return CustomerView.update_customer(
            **params
        )

    def delete(self):
        pass
