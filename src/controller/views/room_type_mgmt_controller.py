from abc import ABC
from logging import getLogger

from flask import request
from flask_jwt_extended import jwt_required

from src.model.views.room_type_mgmt import RoomTypeMgmt
from src.controller.views.view_controller import ViewController
from src.utils.utils import get_params


class RoomTypeMgmtController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    @jwt_required()
    def get(self):
        return self.get_rows(RoomTypeMgmt, getLogger(__name__))

    @jwt_required()
    def post(self):
        excluded_columns = [
            'id',
            'last_modified_at',
            'last_modified_by'
        ]
        params = get_params(request.form, RoomTypeMgmt, excluded_columns)

        self.logger.info(f"New POST request with params: {params}")

        result = RoomTypeMgmt.add_room_type(
            **params
        )

        return result

    @jwt_required()
    def put(self):
        excluded_columns = [
            'last_modified_at',
            'last_modified_by'
        ]
        params = get_params(request.form, RoomTypeMgmt, excluded_columns)

        self.logger.info(f"New PUT request with params: {params}")

        return RoomTypeMgmt.update_room_type(
            **params
        )

    @jwt_required()
    def delete(self):
        pass
