from abc import ABC
from logging import getLogger

from flask import request

from src.model.views.user_view import UserView
from src.controller.views.view_controller import ViewController


class UserViewController(ViewController, ABC):
    def __init__(self):
        self.logger = getLogger(__name__)

    def get(self):
        return self.get_rows(UserView, getLogger(__name__))

    def post(self):
        params = {
            'login': str(request.form['login']),
            'user_password': str(request.form['password']),
        }

        if request.form['customer_last_modified_by'] != '':
            params['last_modified_by_id'] = int(request.form['customer_last_modified_by'])

        self.logger.info(f"New POST request with params: {params}")

        return UserView.add_user(
            **params
        )

    def put(self):
        pass

    def delete(self):
        pass
