from http import HTTPStatus

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from src.controller.types.response import Response
from src.utils.PostgreSQL_errors.pg_error_handler import PostgresErrorHandler

db = SQLAlchemy()
jwt = JWTManager()

HTTPResponse = tuple[Response, HTTPStatus]


def sqlalchemy_error_to_dict(e):
    return (
        jsonify(
            PostgresErrorHandler.getErrorInfo(e)
        )
    )


def get_params(request_form, view_object, excluded_columns) -> dict:
    params = {}
    for key in getViewFields(view_object, excluded_columns):
        params[key] = request_form.get(key, None)
    return params


def getViewFields(class_object, excluded_columns) -> list[str]:
    all_attributes = (dir(class_object))
    field_names = [
        attr for attr in all_attributes
        if not callable(getattr(class_object, attr))
           and not attr.startswith("_")
           and not attr in ['metadata', 'query', 'registry']
           and not attr in excluded_columns
    ]

    return field_names
