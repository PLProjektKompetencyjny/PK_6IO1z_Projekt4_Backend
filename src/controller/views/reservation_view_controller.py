from datetime import datetime
from abc import ABC
from logging import getLogger

from flask import request

from src.model.views.reservation_view import ReservationView
from src.controller.views.view_controller import ViewController
from src.utils.utils import get_params


class ReservationViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        return self.get_rows(ReservationView, getLogger(__name__))

    def post(self):
        excluded_columns = [
            'reservation_id',
            'reservation_status_id',
            'reservation_room_status_id',
            'reservation_last_modified_by',
            'reservation_last_modified_at'
        ]
        params = get_params(request.form, ReservationView, excluded_columns)

        self.logger.info(f"New POST request with params: {params}")

        return ReservationView.add_reservation(
            **params
        )

    def put(self):
        excluded_columns = [
            'reservation_customer_id',
            'reservation_last_modified_by',
            'reservation_last_modified_at'
        ]
        params = get_params(request.form, ReservationView, excluded_columns)

        self.logger.info(f'New PUT request with params: {params}')

        return ReservationView.update_reservation(
            **params
        )

    def delete(self):
        excluded_columns = [
            'reservation_customer_id',
            'reservation_status_id',
            'reservation_number_of_adults',
            'reservation_number_of_children',
            'reservation_start_date',
            'reservation_end_date',
            'reservation_room_status_id',
            'reservation_last_modified_by',
            'reservation_last_modified_at'
        ]
        params = get_params(request.form, ReservationView, excluded_columns)

        self.logger.info(f'New DELETE request with params: {params}')

        return ReservationView.delete_reservation(
            **params
        )
