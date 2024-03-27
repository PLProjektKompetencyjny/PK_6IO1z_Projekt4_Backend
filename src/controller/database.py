from flask import Blueprint, jsonify

from src.model.views.room_view import RoomView

test_database = Blueprint('hello', __name__)


@test_database.route('/rooms', methods=['GET'])
def get_rooms():
    rooms = RoomView.query.all()
    return jsonify(rooms)
