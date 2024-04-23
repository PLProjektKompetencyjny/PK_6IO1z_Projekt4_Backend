from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from src.controller.types.response import Response
from src.controller.enums.http_status_code import HTTPStatusCode
from src.model.views.reservation_view import ReservationView
from src.utils.utils import sqlalchemy_error_to_dict


class ReservationViewController(MethodView):
    @staticmethod
    def get(reservation_id: int = None):
        try:
            if reservation_id is not None:
                db_response = ReservationView.query.get(reservation_id)
            else:
                db_response = ReservationView.query.all()

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            return Response.create(HTTPStatusCode.INTERNAL_SERVER_ERROR.get_value(), json_data_error)

        return Response.create(HTTPStatusCode.OK.get_value(), db_response)
