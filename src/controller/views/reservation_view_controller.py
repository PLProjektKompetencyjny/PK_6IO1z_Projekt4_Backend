import requests

from abc import ABC
from http import HTTPStatus
from logging import getLogger

from flask import request
from flask_jwt_extended import jwt_required

from src.controller.types.response import Response
from src.model.views.customer_view import CustomerView
from src.model.views.invoice_view import InvoiceView
from src.model.views.reservation_view import ReservationView
from src.controller.views.view_controller import ViewController
from src.utils.utils import get_params
from src.service.payments.payments import generate_payment_link_and_update_invoice
from src.model.enums.reservation_status import ReservationStatus


class ReservationViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    @jwt_required()
    def get(self):
        return self.get_rows(ReservationView, getLogger(__name__))

    @jwt_required()
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

        reservation_result = ReservationView.add_reservation(
            **params
        )

        if reservation_result[1] != HTTPStatus.OK:
            return reservation_result

        return reservation_result

    @jwt_required()
    def put(self):
        excluded_columns = [
            'reservation_customer_id',
            'reservation_last_modified_by',
            'reservation_last_modified_at'
        ]

        params = get_params(request.form, ReservationView, excluded_columns)
        reservation_id = params['reservation_id']
        InvoiceView.add_invoice(reservation_id)
        payment_link = generate_payment_link_and_update_invoice(reservation_id)
        self.logger.info(f'New PUT request with params: {params}, Payment link is {payment_link}')
        ReservationView.update_reservation(**params)

        return payment_link

    @jwt_required()
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
