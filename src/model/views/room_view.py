from flask import request
from dataclasses import dataclass
from datetime import datetime

from http import HTTPStatus
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from src.utils.utils import db, HTTPResponse, sqlalchemy_error_to_dict
from src.controller.types.response import Response
from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.controller.views.view_controller import ViewController


@dataclass
class RoomView(db.Model):
    __tablename__ = "room_view"

    room_id: int
    room_type_id: int
    room_status_id: int
    room_number_of_single_beds: int
    room_number_of_double_beds: int
    room_number_of_child_beds: int
    room_gross_price: float
    room_gross_price_adult: float
    room_gross_price_child: float
    room_photos_dir: str
    room_last_modified_by: int
    room_last_modified_at: datetime

    room_id = db.Column("room_id", db.Integer, primary_key=True)
    room_type_id = db.Column("room_type_id", db.Integer)
    room_status_id = db.Column("room_status_id", db.Integer)
    room_number_of_single_beds = db.Column("room_number_of_single_beds", db.Integer)
    room_number_of_double_beds = db.Column("room_number_of_double_beds", db.Integer)
    room_number_of_child_beds = db.Column("room_number_of_child_beds", db.Integer)
    room_gross_price = db.Column("room_gross_price", db.Float)
    room_gross_price_adult = db.Column("room_gross_price_adult", db.Float)
    room_gross_price_child = db.Column("room_gross_price_child", db.Float)
    room_photos_dir = db.Column("room_photos_dir", db.String)
    room_last_modified_by = db.Column("room_last_modified_by", db.String)
    room_last_modified_at = db.Column("room_last_modified_at", db.DateTime)

    def __repr__(self):
        return (
            f"<RoomView(room_id={self.room_id}, "
            f"room_type_id={self.room_type_id}, "
            f"room_status_id={self.room_status_id}, "
            f"room_number_of_single_beds={self.room_number_of_single_beds}, "
            f"room_number_of_double_beds={self.room_number_of_double_beds}, "
            f"room_number_of_child_beds={self.room_number_of_child_beds}, "
            f"room_gross_price={self.room_gross_price}, "
            f"room_gross_price_adult={self.room_gross_price_adult}, "
            f"room_gross_price_child={self.room_gross_price_child}, "
            f"room_photos_dir={self.room_photos_dir}, "
            f"room_last_modified_by={self.room_last_modified_by}, "
            f"room_last_modified_at={self.room_last_modified_at})>"
        )

    @staticmethod
    def check_room_availability(
            room_id: int, start_date: datetime, end_date: datetime
    ) -> int:
        try:
            return db.session.query(
                func.check_room_availability(room_id, start_date, end_date)
            ).scalar()
        except:
            (db.session.rollback())
            return None

    @staticmethod
    def get_available_rooms(logger) -> HTTPResponse:
        filters = request.args.to_dict()
        start_date = filters.get('room_reservation_start_date')
        end_date = filters.get('room_reservation_end_date')
        room_number_of_single_beds = filters.get('room_number_of_single_beds')
        room_number_of_double_beds = filters.get('room_number_of_double_beds')
        room_number_of_child_beds = filters.get('room_number_of_child_beds')

        try:
            rooms = RoomView.query.filter(
                RoomView.room_id == func.check_room_availability(
                    RoomView.room_id,
                    start_date,
                    end_date
                ),
                room_number_of_single_beds is None or RoomView.room_number_of_single_beds == room_number_of_single_beds,
                room_number_of_double_beds is None or RoomView.room_number_of_double_beds == room_number_of_double_beds,
                room_number_of_child_beds is None or RoomView.room_number_of_child_beds == room_number_of_child_beds
            ).all()
            
            return (
                Response.create(
                    DatabaseResponseStatus.OK.get_value(),
                    rooms,
                    DatabaseResponseStatus.OK.get_description(),
                ),
                HTTPStatus.OK,
            )

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            return (
                Response.create(
                    DatabaseResponseStatus.DATABASE_ERROR.get_value(),
                    [],
                    json_data_error.json,
                ),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )
            