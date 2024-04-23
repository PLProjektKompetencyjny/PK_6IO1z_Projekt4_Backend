from flask import request
from flask.views import MethodView
from sqlalchemy import or_, and_, not_, text
from sqlalchemy.exc import SQLAlchemyError

from logging import getLogger
from http import HTTPStatus
from abc import ABC, abstractmethod

from src.controller.types.response import Response
from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.utils.utils import sqlalchemy_error_to_dict


class ViewController(ABC, MethodView):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def post(self):
        pass

    @abstractmethod
    def put(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @staticmethod
    def apply_model_filters(model, filters):
        query = model.query

        filters_handlers = {
            '!': lambda field, value: field != value,
            '*': lambda field, value: field.like(f"%{value}%"),
            '<': lambda field, value: field < value,
            '>': lambda field, value: field > value,
        }

        for key, value in filters.items():
            operator = value[0]

            if operator in filters_handlers:
                value = value.replace(operator, '')
                query = query.filter(filters_handlers[operator](model.__table__.c[key], value))
            else:
                query = query.filter(model.__table__.c[key] == value)

        return query

    def get_rows(self, model, logger):
        filters = request.args.to_dict()

        try:
            query = self.apply_model_filters(model, filters)
            db_response = query.all()

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            return Response.create(DatabaseResponseStatus.DATABASE_ERROR.get_value(), [],
                                   json_data_error.json), HTTPStatus.OK

        row_count = len(db_response)

        if not row_count:
            logger.error(f"No rows found in [{model.__tablename__}] with filters [{filters}]")
            return Response.create(DatabaseResponseStatus.NOT_FOUND.get_value(), [],
                                   DatabaseResponseStatus.NOT_FOUND.get_description()), HTTPStatus.OK

        logger.info(f"Found [{row_count}] rows in [{model.__tablename__}] with filters [{filters}]")
        return Response.create(DatabaseResponseStatus.OK.get_value(), db_response,
                               DatabaseResponseStatus.OK.get_description()), HTTPStatus.OK
