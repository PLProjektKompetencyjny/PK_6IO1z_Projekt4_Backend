from abc import ABC
from logging import getLogger

from src.model.views.room_view import RoomView
from src.controller.views.view_controller import ViewController


class RoomViewController(ViewController, ABC):
    def get(self):
        return self.get_rows(RoomView, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
