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
