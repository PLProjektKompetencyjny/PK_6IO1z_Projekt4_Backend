from abc import ABC
from logging import getLogger

from src.model.views.room_mgmt import RoomMgmt
from src.controller.views.view_controller import ViewController


class RoomMgmtController(ViewController, ABC):
    def get(self):
        return self.get_rows(RoomMgmt, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
