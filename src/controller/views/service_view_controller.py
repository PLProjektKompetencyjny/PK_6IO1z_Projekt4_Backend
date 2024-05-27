from flask import request
from abc import ABC
from logging import getLogger

from src.model.views.service_view import ServiceView
from src.controller.views.view_controller import ViewController


class ServiceViewController(ViewController, ABC):
    def get(self):
        if len(request.args.to_dict().items()) == 0:
            return ServiceView.get_available_services(ServiceView, getLogger(__name__))
        
        return self.get_rows(ServiceView, getLogger(__name__))

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
