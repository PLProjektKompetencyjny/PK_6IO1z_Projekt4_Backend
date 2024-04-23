from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from src.model.views.customer_view import CustomerView
from src.controller.types.response import Response
from src.controller.enums.http_status_code import HTTPStatusCode
from src.utils.utils import sqlalchemy_error_to_dict


class CustomerViewController(MethodView):
    @staticmethod
    def get(customer_id: int = None):
        try:
            if customer_id is not None:
                db_response = CustomerView.query.get(customer_id)
            else:
                db_response = CustomerView.query.all()

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            return Response.create(HTTPStatusCode.INTERNAL_SERVER_ERROR.get_value(), json_data_error)

        return Response.create(HTTPStatusCode.OK.get_value(), db_response)
