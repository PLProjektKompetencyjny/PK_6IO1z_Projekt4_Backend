from abc import ABC
from logging import getLogger

from flask import request

from src.model.views.customer_view import CustomerView
from src.controller.views.view_controller import ViewController


class CustomerViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        return self.get_rows(CustomerView, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        params = {
            'customer_id': int(request.form['customer_id']),
            'customer_name': str(request.form['customer_name']),
            'customer_surname': str(request.form['customer_surname']),
            'customer_phone': str(request.form['customer_phone']),
            'customer_city': str(request.form['customer_city']),
            'customer_postal_code': str(request.form['customer_postal_code']),
            'customer_street': str(request.form['customer_street']),
            'customer_building_number': str(request.form['customer_building_number']),
        }

        if request.form['customer_nip_number'] != '':
            params['customer_nip_number'] = str(request.form['customer_nip_number'])
        else:
            params['customer_nip_number'] = None

        if request.form['customer_last_modified_by'] != '':
            params['customer_last_modified_by'] = int(request.form['customer_last_modified_by'])
        else:
            params['customer_last_modified_by'] = None

        self.logger.info(f"New PUT request with params: {params}")

        return CustomerView.update_customer(
            **params
        )

    def delete(self):
        pass
