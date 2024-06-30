from flask import request
from abc import ABC
from logging import getLogger

from src.model.views.service_view import ServiceView
from src.controller.views.view_controller import ViewController
from src.utils.utils import get_params


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
        excluded_columns = [
            'service_name',
            'service_price',
            'service_last_modified_at',
            'service_last_modified_by'
        ]

        params = get_params(request.form, ServiceView, excluded_columns)

        self.logger.info(f"New POST request with params: {params}")

        return ServiceView.add_service(
            **params
        )

    def put(self):
        pass

    def delete(self):
        pass
