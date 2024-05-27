from abc import ABC
from logging import getLogger

from src.model.views.room_type_mgmt import RoomTypeMgmt
from src.controller.views.view_controller import ViewController


class RoomTypeMgmtController(ViewController, ABC):
    def get(self):
        return self.get_rows(RoomTypeMgmt, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
