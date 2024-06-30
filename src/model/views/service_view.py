from dataclasses import dataclass
from datetime import datetime

from http import HTTPStatus
from sqlalchemy.exc import SQLAlchemyError

from src.utils.utils import db, HTTPResponse
from src.controller.db_handler import DBHandler
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
    def get_available_services(logger) -> HTTPResponse:
        service_id = 'service_id'
        service_name = 'service_name'
        unit_price = 'unit_price'

        try:
            db_output = DBHandler.get_available_services()

            db_response = [
                {
                    f'{service_id}': item[0],
                    f'{service_name}': item[1],
                    f'{unit_price}': item[2]
                }
                for item in db_output
            ]

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            return (
                Response.create(
                    DatabaseResponseStatus.DATABASE_ERROR.get_value(),
                    [],
                    json_data_error.json),
                HTTPStatus.INTERNAL_SERVER_ERROR
            )

        row_count = len(db_response)

        if row_count == 0:
            logger.info(f"Could not find any available services")

            return (
                Response.create(
                    DatabaseResponseStatus.NOT_FOUND.get_value(),
                    [],
                    DatabaseResponseStatus.NOT_FOUND.get_description()),
                HTTPStatus.OK
            )

        logger.info(f"Found [{row_count}] available services: {db_response}")

        return (
            Response.create(
                DatabaseResponseStatus.OK.get_value(),
                db_response,
                DatabaseResponseStatus.OK.get_description()),
            HTTPStatus.OK
        )

    @staticmethod
    def add_service(service_reservation_id: int,
                    service_id: int,
                    service_quantity: int) -> HTTPResponse:
        sql = (
            f"""
            INSERT INTO service_view (
                service_reservation_id, 
                service_id, 
                service_quantity
            )
            VALUES (
                {service_reservation_id}, 
                {service_id}, 
                {service_quantity}
            )
            """
        )

        return DBHandler.run_sql_query(sql)
