from abc import ABC
from logging import getLogger

from flask import request
from flask_jwt_extended import jwt_required

from src.model.views.room_mgmt import RoomMgmt
from src.controller.views.view_controller import ViewController
from src.utils.utils import get_params


class RoomMgmtController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    @jwt_required()
    def get(self):
        return self.get_rows(RoomMgmt, getLogger(__name__))

    @jwt_required()
    def post(self):
        excluded_columns = [
            'id',
            'last_modified_by',
            'last_modified_at'
        ]

        params = get_params(request.form, RoomMgmt, excluded_columns)

        self.logger.info(f"New POST request with params: {params}")

        return RoomMgmt.add_room(
            **params
        )

    @jwt_required()
    def put(self):
        excluded_columns = [
            'last_modified_by',
            'last_modified_at'
        ]

        params = get_params(request.form, RoomMgmt, excluded_columns)

        self.logger.info(f"New PUT request with params: {params}")

        return RoomMgmt.update_room(
            **params
        )

    @jwt_required()
    def delete(self):
        pass
