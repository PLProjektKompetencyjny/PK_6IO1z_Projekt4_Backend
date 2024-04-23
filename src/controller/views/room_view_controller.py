from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from src.controller.response import Response
from src.controller.types.http_status_code import HTTPStatusCode
from src.model.views.room_view import RoomView
from src.utils.utils import sqlalchemy_error_to_dict


class RoomViewController(MethodView):
    @staticmethod
    def get(room_id: int = None):
        try:
            if room_id is not None:
                db_response = RoomView.query.get(room_id)
            else:
                db_response = RoomView.query.all()

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            return Response.create(HTTPStatusCode.INTERNAL_SERVER_ERROR.get_value(), json_data_error)

        return Response.create(HTTPStatusCode.OK.get_value(), db_response)
