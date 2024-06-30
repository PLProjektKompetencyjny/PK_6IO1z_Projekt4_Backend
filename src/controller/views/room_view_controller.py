from abc import ABC
from logging import getLogger
from flask import request

from http import HTTPStatus

from src.model.views.room_view import RoomView
from src.controller.views.view_controller import ViewController

from src.controller.types.response import Response
from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.utils.utils import sqlalchemy_error_to_dict


class RoomViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        return RoomView.get_available_rooms(getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
