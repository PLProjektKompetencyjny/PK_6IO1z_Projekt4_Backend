from flask import request
from abc import ABC
from logging import getLogger

from src.model.views.service_view import ServiceView
from src.controller.views.view_controller import ViewController


class ServiceViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        if len(request.args.to_dict().items()) == 0:
            return ServiceView.get_available_services(ServiceView, getLogger(__name__))

        return self.get_rows(ServiceView, getLogger(__name__))

    def post(self):
        params = {
            "reservation_id": int(request.form['reservation_id']),
            "sid": int(request.form['id']),
            "quantity": int(request.form['quantity']),
        }

        self.logger.info(f"New POST request with params: {params}")

        result = ServiceView.add_service(
            **params
        )

        return result

    def put(self):
        pass

    def delete(self):
        pass
