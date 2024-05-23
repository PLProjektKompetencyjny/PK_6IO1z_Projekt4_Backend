from flask import Blueprint

from src.controller.views.customer_view_controller import CustomerViewController
from src.controller.views.room_view_controller import RoomViewController
from src.controller.views.invoice_view_controller import InvoiceViewController
from src.controller.views.user_view_controller import UserViewController
from src.controller.views.reservation_view_controller import ReservationViewController

database = Blueprint('database', __name__, url_prefix='/api')

database.add_url_rule('/customers', view_func=CustomerViewController.as_view('customers'), methods=['GET'])

database.add_url_rule('/rooms', view_func=RoomViewController.as_view('rooms'), methods=['GET'])

database.add_url_rule('/invoices', view_func=InvoiceViewController.as_view('invoices'), methods=['GET'])

database.add_url_rule('/users', view_func=UserViewController.as_view('users'), methods=['GET'])

database.add_url_rule('/reservations', view_func=ReservationViewController.as_view('reservations'), methods=['GET'])
