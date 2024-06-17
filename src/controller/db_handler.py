from http import HTTPStatus
from logging import getLogger

from sqlalchemy import text, func
from sqlalchemy.exc import SQLAlchemyError

from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.controller.types.response import Response
from src.utils.utils import db, sqlalchemy_error_to_dict


class DBHandler:
    @staticmethod
    def run_sql_query(query: str) -> tuple[Response, HTTPStatus]:
        try:
            db.session.execute(text(query))
            db.session.commit()

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            getLogger(__name__).error(json_data_error.json)
            db.session.rollback()

            return (
                Response.create(
                    DatabaseResponseStatus.DATABASE_ERROR.get_value(),
                    [],
                    json_data_error.json),
                HTTPStatus.INTERNAL_SERVER_ERROR)

        return (
            Response.create(
                DatabaseResponseStatus.OK.get_value(),
                [],
                DatabaseResponseStatus.OK.get_description(),
            ),
            HTTPStatus.OK,
        )

    @staticmethod
    def run_sql_query_raw(query: str) -> int:
        try:
            db.session.execute(text(query))
            db.session.commit()

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            getLogger(__name__).error(json_data_error.json)
            db.session.rollback()

            return 1

        return 0

    @staticmethod
    def run_sql_function_all(db_function, *args):
        try:
            db.session.query(
                db_function(*args)
            ).all()

            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            json_data_error = sqlalchemy_error_to_dict(e)
            getLogger(__name__).error(json_data_error.json)
            db.session.rollback()

            return (Response.create(
                DatabaseResponseStatus.DATABASE_ERROR.get_value(),
                [],
                json_data_error.json),
                    HTTPStatus.INTERNAL_SERVER_ERROR)

        return (
            Response.create(
                DatabaseResponseStatus.OK.get_value(),
                [],
                DatabaseResponseStatus.OK.get_description(),
            ),
            HTTPStatus.OK,
        )

    @staticmethod
    def run_sql_function_scalar(db_function: func, *args):
        try:
            result = db.session.query(
                db_function(*args)
            ).scalar()

            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            json_data_error = sqlalchemy_error_to_dict(e)
            getLogger(__name__).error(json_data_error.json)
            db.session.rollback()

            return (Response.create(
                DatabaseResponseStatus.DATABASE_ERROR.get_value(),
                [],
                json_data_error.json),
                    HTTPStatus.INTERNAL_SERVER_ERROR)

        return (
            Response.create(
                DatabaseResponseStatus.OK.get_value(),
                [{
                    'function_name': db_function._FuncionGenerator._FunctionGenerator__names[0],
                    'result': result
                }],
                DatabaseResponseStatus.OK.get_description(),
            ),
            HTTPStatus.OK,
        )

    @staticmethod
    def get_available_services():
        try:
            db_output = (
                db.session.query(
                    func
                    .get_available_services()
                    .table_valued(
                        'service_id',
                        'service_name',
                        'unit_price'
                    )
                )
            ).all()

        except SQLAlchemyError as e:
            raise e

        return db_output
