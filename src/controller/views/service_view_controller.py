from flask import request
from abc import ABC
from logging import getLogger

from flask_jwt_extended import jwt_required

from src.model.views.service_view import ServiceView
from src.controller.views.view_controller import ViewController
from src.utils.utils import get_params


class ServiceViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    @jwt_required()
    def get(self):
        params = request.args.to_dict()

        self.logger.info(f"New GET request with params: {params}")

        if len(params.items()) == 0:
            return ServiceView.get_available_services(self.logger)

        return self.get_rows(ServiceView, self.logger)

    @jwt_required()
    def post(self):
        excluded_columns = [
            'service_name',
            'service_price',
            'service_price_total',
            'service_last_modified_at',
            'service_last_modified_by'
        ]

        params = get_params(request.form, ServiceView, excluded_columns)

        self.logger.info(f"New POST request with params: {params}")

        return ServiceView.add_service(
            **params
        )

    @jwt_required()
    def put(self):
        excluded_columns = [
            'service_name',
            'service_price',
            'service_price_total',
            'service_last_modified_at',
            'service_last_modified_by'
        ]
        params = get_params(request.form, ServiceView, excluded_columns)

        self.logger.info(f"New PUT request with params: {params}")

        return ServiceView.update_service(
            **params
        )

    @jwt_required()
    def delete(self):
        excluded_columns = [
            'service_name',
            'service_price',
            'service_price_total',
            'service_quantity',
            'service_last_modified_by',
            'service_last_modified_at'
        ]
        params = get_params(request.form, ServiceView, excluded_columns)

        self.logger.info(f"New DELETE request with params: {params}")

        return ServiceView.delete_service(
            **params
        )
