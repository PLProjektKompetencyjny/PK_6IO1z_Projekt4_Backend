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
        filters = request.args.to_dict()

        if filters.get('room_reservation_start_date') is not None and filters.get('room_reservation_end_date') is not None:
            return RoomView.get_available_rooms(self.logger)

        return self.get_rows(RoomView, self.logger)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
