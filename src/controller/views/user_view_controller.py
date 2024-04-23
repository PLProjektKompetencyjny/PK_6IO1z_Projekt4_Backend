from abc import ABC
from logging import getLogger

from flask import jsonify

from src.model.views.user_view import UserView
from src.controller.views.view_controller import ViewController


class UserViewController(ViewController, ABC):
    def get(self):
        return self.get_single_or_all_rows(UserView, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
