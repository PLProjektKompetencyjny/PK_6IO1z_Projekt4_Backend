from abc import ABC
from logging import getLogger

from src.model.views.reservation_view import ReservationView
from src.controller.views.view_controller import ViewController


class ReservationViewController(ViewController, ABC):
    def get(self):
        return self.get_single_or_all_rows(ReservationView, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
