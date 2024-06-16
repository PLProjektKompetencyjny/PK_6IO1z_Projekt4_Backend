from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from logging import getLogger

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.controller.types.response import Response
from src.utils.utils import db, sqlalchemy_error_to_dict


@dataclass
class RoomTypeMgmt(db.Model):
    __tablename__ = 'room_type_mgmt'

    id: int
    num_of_single_beds: int
    num_of_double_beds: int
    num_of_child_beds: int
    adult_price_gross: float
    child_price_gross: float
    photos_dir: str
    last_modified_by: int
    last_modified_at: datetime

    id = db.Column('id', db.Integer, primary_key=True)
    num_of_single_beds = db.Column('num_of_single_beds', db.Integer)
    num_of_double_beds = db.Column('num_of_double_beds', db.Integer)
    num_of_child_beds = db.Column('num_of_child_beds', db.Integer)
    adult_price_gross = db.Column('adult_price_gross', db.Float)
    child_price_gross = db.Column('child_price_gross', db.Float)
    photos_dir = db.Column('photos_dir', db.String)
    last_modified_by = db.Column('last_modified_by', db.String)
    last_modified_at = db.Column('last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<RoomTypeMgmt(id={self.id}, '
            f'num_of_single_beds={self.num_of_single_beds}, '
            f'num_of_double_beds={self.num_of_double_beds}, '
            f'num_of_child_beds={self.num_of_child_beds}, '
            f'adult_price_gross={self.adult_price_gross}, '
            f'child_price_gross={self.child_price_gross}, '
            f'photos_dir={self.photos_dir}, '
            f'last_modified_by={self.last_modified_by}, '
            f'last_modified_at={self.last_modified_at}>'
        )

    @staticmethod
    def add_room_type(num_of_single_beds: int,
                      num_of_double_beds: int,
                      num_of_child_beds: int,
                      adult_price_gross: float,
                      child_price_gross: float,
                      photos_dir: str) -> tuple[Response, HTTPStatus]:

        sql = text(
            f"""    
            INSERT INTO room_type_mgmt (
            num_of_single_beds, 
            num_of_double_beds, 
            num_of_child_beds, 
            adult_price_gross, 
            child_price_gross, photos_dir)
            VALUES (
            {num_of_single_beds},
            {num_of_double_beds},
            {num_of_child_beds},
            {adult_price_gross},
            {child_price_gross},
            '{photos_dir}'
            )
            """
        )

        try:
            db.session.execute(sql)
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
    def update_room_type(room_type_id: int,
                         num_of_single_beds: int,
                         num_of_double_beds: int,
                         num_of_child_beds: int,
                         adult_price_gross: float,
                         child_price_gross: float,
                         photos_dir: str) -> tuple[Response, HTTPStatus]:

        sql = text(
            f"""    
            UPDATE room_type_mgmt 
            SET 
                num_of_single_beds = {num_of_single_beds},
                num_of_double_beds = {num_of_double_beds},
                num_of_child_beds = {num_of_child_beds},
                adult_price_gross = {adult_price_gross},
                child_price_gross = {child_price_gross},
                photos_dir = '{photos_dir}'
            WHERE 
                id = {room_type_id}
            """
        )

        try:
            db.session.execute(sql)
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
