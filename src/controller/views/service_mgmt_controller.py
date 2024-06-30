from abc import ABC
from logging import getLogger

from src.model.views.service_mgmt import ServiceMgmt
from src.controller.views.view_controller import ViewController


class ServiceMgmtController(ViewController, ABC):
    def get(self):
        return self.get_rows(ServiceMgmt, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
