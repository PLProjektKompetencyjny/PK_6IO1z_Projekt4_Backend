from flask import request
from abc import ABC
from logging import getLogger

from src.model.views.service_view import ServiceView
from src.controller.views.view_controller import ViewController


class ServiceViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        params = request.args.to_dict()

        self.logger.info(f"New GET request with params: {params}")

        if len(params.items()) == 0:
            return ServiceView.get_available_services(getLogger(__name__))

        return self.get_rows(ServiceView, getLogger(__name__))

    def post(self):
        params = {
            "reservation_id": int(request.form['reservation_id']),
            "sid": int(request.form['id']),
            "quantity": int(request.form['quantity']),
        }

        self.logger.info(f"New POST request with params: {params}")

        return ServiceView.add_service(
            **params
        )

    def put(self):
        pass

    def delete(self):
        pass
