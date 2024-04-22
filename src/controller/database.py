from flask import Blueprint, jsonify

from src.model.views.room_view import RoomView
from src.model.views.invoice_view import InvoiceView
from src.model.views.reservation_view import ReservationView
from src.model.views.user_view import UserView
from src.model.views.customer_view import CustomerView

database = Blueprint('hello', __name__)


@database.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = RoomView.query.all()
    return jsonify(rooms)


@database.route('/invoices', methods=['GET'])
def get_invoices():
    invoices = InvoiceView.query.all()
    return jsonify(invoices)


@database.route('/users', methods=['GET'])
def get_users():
    users = UserView.query.all()
    return jsonify(users)


@database.route('/customers', methods=['GET'])
def get_customers():
    customers = CustomerView.query.all()
    return jsonify(customers)


@database.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = ReservationView.query.all()
    return jsonify(reservations)
