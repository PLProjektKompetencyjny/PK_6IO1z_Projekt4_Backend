from abc import ABC
from logging import getLogger

from src.model.views.service_view import ServiceView
from src.controller.views.view_controller import ViewController


class ServiceViewController(ViewController, ABC):
    def get(self):
        return self.get_rows(ServiceView, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
