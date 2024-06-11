from flask import Blueprint

from src.controller.views.customer_view_controller import CustomerViewController
from src.controller.views.room_view_controller import RoomViewController
from src.controller.views.invoice_view_controller import InvoiceViewController
from src.controller.views.user_view_controller import UserViewController
from src.controller.views.reservation_view_controller import ReservationViewController
from src.controller.views.service_view_controller import ServiceViewController
from src.controller.views.room_type_mgmt_controller import RoomTypeMgmtController
from src.controller.views.room_mgmt_controller import RoomMgmtController
from src.controller.views.service_mgmt_controller import ServiceMgmtController

database = Blueprint('database', __name__, url_prefix='/api')

database.add_url_rule('/customers', view_func=CustomerViewController.as_view('customers'), methods=['GET'])

database.add_url_rule('/rooms', view_func=RoomViewController.as_view('rooms'), methods=['GET'])

database.add_url_rule('/invoices', view_func=InvoiceViewController.as_view('invoices'), methods=['GET', 'POST', 'PUT'])

database.add_url_rule('/users', view_func=UserViewController.as_view('users'), methods=['GET'])

database.add_url_rule('/reservations', view_func=ReservationViewController.as_view('reservations'),
                      methods=['GET', 'POST'])

database.add_url_rule('/services', view_func=ServiceViewController.as_view('services'), methods=['GET', 'POST'])

database.add_url_rule('/admin/room_type', view_func=RoomTypeMgmtController.as_view('room_type'), methods=['GET'])

database.add_url_rule('/admin/room', view_func=RoomMgmtController.as_view('room'), methods=['GET'])

database.add_url_rule('/admin/service', view_func=ServiceMgmtController.as_view('service'), methods=['GET'])
