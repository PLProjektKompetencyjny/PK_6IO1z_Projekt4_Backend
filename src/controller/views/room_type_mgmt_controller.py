from abc import ABC
from logging import getLogger

from flask import request

from src.model.views.room_type_mgmt import RoomTypeMgmt
from src.controller.views.view_controller import ViewController


class RoomTypeMgmtController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        return self.get_rows(RoomTypeMgmt, getLogger(__name__))

    def post(self):
        params = {
            'num_of_single_beds': int(request.form['num_of_single_beds']),
            'num_of_double_beds': str(request.form['num_of_double_beds']),
            'num_of_child_beds': str(request.form['num_of_child_beds']),
            'adult_price_gross': str(request.form['adult_price_gross']),
            'child_price_gross': str(request.form['child_price_gross']),
            'photos_dir': str(request.form['photos_dir']),
        }

        self.logger.info(f"New POST request with params: {params}")

        result = RoomTypeMgmt.add_room_type(
            **params
        )

        return result

    def put(self):
        params = {
            'room_type_id': int(request.form['id']),
            'num_of_single_beds': int(request.form['num_of_single_beds']),
            'num_of_double_beds': str(request.form['num_of_double_beds']),
            'num_of_child_beds': str(request.form['num_of_child_beds']),
            'adult_price_gross': str(request.form['adult_price_gross']),
            'child_price_gross': str(request.form['child_price_gross']),
            'photos_dir': str(request.form['photos_dir']),
        }

        self.logger.info(f"New POST request with params: {params}")

        return RoomTypeMgmt.update_room_type(
            **params
        )

    def delete(self):
        pass
