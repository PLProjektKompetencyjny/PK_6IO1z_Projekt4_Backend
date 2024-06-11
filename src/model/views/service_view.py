from logging import getLogger

from flask import request
from dataclasses import dataclass
from datetime import datetime

from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError

from src.utils.utils import db
from sqlalchemy import func

from src.controller.types.response import Response
from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.utils.utils import sqlalchemy_error_to_dict


@dataclass
class ServiceView(db.Model):
    __tablename__ = 'service_view'

    service_id: int
    service_name: str
    service_price: float
    service_reservation_id: int
    service_quantity: int
    service_last_modified_by: int
    service_last_modified_at: datetime

    service_id = db.Column('service_id', db.Integer, primary_key=True)
    service_name = db.Column('service_name', db.String)
    service_price = db.Column('service_price', db.Float)
    service_reservation_id = db.Column('service_reservation_id', db.Integer, primary_key=True)
    service_quantity = db.Column('service_quantity', db.Float)
    service_last_modified_by = db.Column('service_last_modified_by', db.String)
    service_last_modified_at = db.Column('service_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<ServiceView(service_id={self.service_id}, '
            f'service_name={self.service_name}, '
            f'service_price={self.service_price}, '
            f'service_reservation_id={self.service_reservation_id}, '
            f'service_quantity={self.service_quantity}, '
            f'service_last_modified_by={self.service_last_modified_by}, '
            f'service_last_modified_at={self.service_last_modified_at})>'
        )

    @staticmethod
    def get_available_services(model, logger) -> tuple[Response, HTTPStatus]:
        filters = request.args.to_dict()
        db_response = None

        try:
            db_output = (
                db
                .session
                .query(
                    func
                    .get_available_services()
                    .table_valued(
                        'service_id',
                        'service_name',
                        'unit_price'
                    )
                )
                .all()
            )
            db_response = []
            for item in db_output:
                db_response.append(
                    ServiceView(
                        **{
                            "service_id": item[0],
                            "service_name": item[1],
                            "service_price": item[2]
                        }
                    )
                )
        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            return (
                Response.create(
                    DatabaseResponseStatus.DATABASE_ERROR.get_value(), [],
                    json_data_error.json),
                HTTPStatus.OK)

        row_count = len(db_response)

        if not row_count:
            logger.error(f"No rows found in [{model.__tablename__}] with filters [{filters}]")

            return (
                Response.create(
                    DatabaseResponseStatus.NOT_FOUND.get_value(),
                    [],
                    DatabaseResponseStatus.NOT_FOUND.get_description()),
                HTTPStatus.OK)

        logger.info(f"Found [{row_count}] rows in [{model.__tablename__}] with filters [{filters}]")

        return (
            Response.create(
                DatabaseResponseStatus.OK.get_value(),
                db_response,
                DatabaseResponseStatus.OK.get_description()),
            HTTPStatus.OK)

    @staticmethod
    def add_service(reservation_id: int, sid: int, quantity: int) -> tuple[Response, HTTPStatus]:
        entry = ServiceView(
            service_reservation_id=reservation_id,
            service_id=sid,
            service_quantity=quantity
        )

        try:
            db.session.add(entry)
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
