from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from logging import getLogger

from flask import Response
from sqlalchemy.exc import SQLAlchemyError

from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.controller.types.response import Response
from src.utils.utils import db, sqlalchemy_error_to_dict


@dataclass
class ReservationView(db.Model):
    __tablename__ = 'reservation_view'

    reservation_id: int
    reservation_customer_id: int
    reservation_status_id: int
    reservation_number_of_adults: int
    reservation_number_of_children: int
    reservation_start_date: datetime
    reservation_end_date: datetime
    reservation_room_id: int
    reservation_room_status_id: int
    reservation_last_modified_by: int
    reservation_last_modified_at: datetime

    reservation_id = db.Column('reservation_id', db.Integer, primary_key=True, autoincrement=True)
    reservation_customer_id = db.Column('reservation_customer_id', db.Integer)
    reservation_status_id = db.Column('reservation_status_id', db.Integer)
    reservation_number_of_adults = db.Column('room_number_of_adults', db.Integer)
    reservation_number_of_children = db.Column('room_number_of_children', db.Integer)
    reservation_start_date = db.Column('reservation_start_date', db.DateTime)
    reservation_end_date = db.Column('reservation_end_date', db.DateTime)
    reservation_room_id = db.Column('reservation_room_id', db.Integer, primary_key=True)
    reservation_room_status_id = db.Column('reservation_room_status_id', db.Integer)
    reservation_last_modified_by = db.Column('reservation_last_modified_by', db.String)
    reservation_last_modified_at = db.Column('reservation_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<ReservationView(reservation_id={self.reservation_id}, '
            f'reservation_customer_id={self.reservation_customer_id}, '
            f'reservation_status_id={self.reservation_status_id}, '
            f'reservation_number_of_adults={self.reservation_number_of_adults}, '
            f'reservation_number_of_children={self.reservation_number_of_children}, '
            f'reservation_start_date={self.reservation_start_date}, '
            f'reservation_end_date={self.reservation_end_date}, '
            f'reservation_room_id={self.reservation_room_id}, '
            f'reservation_room_status_id={self.reservation_room_status_id}, '
            f'reservation_last_modified_by={self.reservation_last_modified_by}, '
            f'reservation_last_modified_at={self.reservation_last_modified_at})>'
        )

    @staticmethod
    def add_reservation(customer_id: int, number_of_adults: int, number_of_children: int,
                        start_date: datetime.date,
                        end_date: datetime.date, room_id: int) -> tuple[Response, HTTPStatus]:

        entry = ReservationView(
            reservation_customer_id=customer_id,
            reservation_number_of_adults=number_of_adults,
            reservation_number_of_children=number_of_children,
            reservation_start_date=start_date,
            reservation_end_date=end_date,
            reservation_room_id=room_id
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
