from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
from celery.beat import Service
from flask import request

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

    service_id = db.Column('service_id', db.Integer, primary_key=True)
    service_name = db.Column('service_name', db.String)
    service_price = db.Column('service_price', db.Float)
    service_price_total = db.Column('service_price_total', db.Float)
    service_reservation_id = db.Column('service_reservation_id', db.Integer, primary_key=True)
    service_quantity = db.Column('service_quantity', db.Float)
    service_last_modified_by = db.Column('service_last_modified_by', db.String)
    service_last_modified_at = db.Column('service_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<ServiceView(service_id={self.service_id}, '
            f'service_name={self.service_name}, '
            f'service_price={self.service_price}, '
            f'service_price_total={self.service_price_total},'
            f'service_reservation_id={self.service_reservation_id}, '
            f'service_quantity={self.service_quantity}, '
            f'service_last_modified_by={self.service_last_modified_by}, '
            f'service_last_modified_at={self.service_last_modified_at})>'
        )

    @staticmethod
    def get_available_services(logger) -> HTTPResponse:
        if logger is None:
            logger = getLogger(__name__)
        
        service_id = 'service_id'
        service_name = 'service_name'
        service_price = 'service_price'

        try:
            db_output = DBHandler.get_available_services()

            db_response = [
                {
                    f'{service_id}': item[0],
                    f'{service_name}': item[1],
                    f'{service_price}': item[2]
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

    @staticmethod
    def update_service(service_id: int,
                       service_reservation_id: int,
                       service_quantity: float) -> HTTPResponse:
        sql = (
            f"""
            UPDATE 
                service_view
            SET
                service_quantity = {service_quantity}
            WHERE 
                service_id = {service_id}
                AND service_reservation_id = {service_reservation_id}
            """
        )

        return DBHandler.run_sql_query(sql)

    @staticmethod
    def delete_service(service_id: int, service_reservation_id: int) -> HTTPResponse:
        sql = (
            f"""
                DELETE FROM 
                    service_view
                WHERE 
                    service_id = {service_id}
                    AND service_reservation_id = {service_reservation_id}
                """
        )

        return DBHandler.run_sql_query(sql)

    @staticmethod
    def get_services_by_reservation_id(reservation_id: int, logger):
        try:
            rows = db.session.query(ServiceView.service_name.label('service_name'),
                                    ServiceView.service_price.label('service_price'),
                                    ServiceView.service_quantity.label('service_quantity'),
                                    ServiceView.service_price_total.label('service_price_total')
                                    ).filter(ServiceView.service_reservation_id == reservation_id
                                             ).all()
        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            raise e

        if rows is None:
            raise NoResultFound

        return rows
