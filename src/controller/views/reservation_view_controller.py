from datetime import datetime
from abc import ABC
from logging import getLogger

from flask import request

from src.model.views.reservation_view import ReservationView
from src.controller.views.view_controller import ViewController


class ReservationViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        return self.get_rows(ReservationView, getLogger(__name__))

    def post(self):
        params = {
            "customer_id": int(request.form['reservation_customer_id']),
            "number_of_adults": int(request.form['reservation_number_of_adults']),
            "number_of_children": int(request.form['reservation_number_of_children']),
            "start_date": datetime.strptime(request.form['reservation_start_date'], '%d-%m-%Y'),
            "end_date": datetime.strptime(request.form['reservation_end_date'], '%d-%m-%Y'),
            "room_id": int(request.form['reservation_room_id'])
        }

        self.logger.info(f"New POST request with params: {params}")

        return ReservationView.add_reservation(
            **params
        )

    def put(self):
        pass

    def delete(self):
        pass
