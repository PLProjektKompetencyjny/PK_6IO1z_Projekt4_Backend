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


def getViewFields(classObject, excludedColumns) -> list[str]:
    all_attributes = (dir(classObject))
    field_names = [
        attr for attr in all_attributes
        if not callable(getattr(classObject, attr))
        and not attr.startswith("_")
        and not attr in ['metadata', 'query', 'registry']
        and not attr in excludedColumns
    ]
    
    return field_names
