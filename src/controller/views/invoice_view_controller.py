from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from src.controller.response import Response
from src.controller.types.http_status_code import HTTPStatusCode
from src.model.views.invoice_view import InvoiceView
from src.utils.utils import sqlalchemy_error_to_dict


class InvoiceViewController(MethodView):
    @staticmethod
    def get(invoice_id: int = None):
        try:
            if invoice_id is not None:
                db_response = InvoiceView.query.get(invoice_id)
            else:
                db_response = InvoiceView.query.all()

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            return Response.create(HTTPStatusCode.INTERNAL_SERVER_ERROR.get_value(), json_data_error)

        return Response.create(HTTPStatusCode.OK.get_value(), db_response)
