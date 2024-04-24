from dataclasses import dataclass
from datetime import datetime

from src.utils.utils import db


@dataclass
class RoomView(db.Model):
    __tablename__ = 'room_view'

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

    room_id = db.Column('room_id', db.Integer, primary_key=True)
    room_type_id = db.Column('room_type_id', db.Integer)
    room_status_id = db.Column('room_status_id', db.Integer)
    room_number_of_single_beds = db.Column('room_number_of_single_beds', db.Integer)
    room_number_of_double_beds = db.Column('room_number_of_double_beds', db.Integer)
    room_number_of_child_beds = db.Column('room_number_of_child_beds', db.Integer)
    room_gross_price = db.Column('room_gross_price', db.Float)
    room_gross_price_adult = db.Column('room_gross_price_adult', db.Float)
    room_gross_price_child = db.Column('room_gross_price_child', db.Float)
    room_photos_dir = db.Column('room_photos_dir', db.String)
    room_last_modified_by = db.Column('room_last_modified_by', db.String, nullable=True)
    room_last_modified_at = db.Column('room_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<RoomView(room_id={self.room_id}, '
            f'room_type_id={self.room_type_id}, '
            f'room_status_id={self.room_status_id}, '
            f'room_number_of_single_beds={self.room_number_of_single_beds}, '
            f'room_number_of_double_beds={self.room_number_of_double_beds}, '
            f'room_number_of_child_beds={self.room_number_of_child_beds}, '
            f'room_gross_price={self.room_gross_price}, '
            f'room_gross_price_adult={self.room_gross_price_adult}, '
            f'room_gross_price_child={self.room_gross_price_child}, '
            f'room_photos_dir={self.room_photos_dir}, '
            f'room_last_modified_by={self.room_last_modified_by}, '
            f'room_last_modified_at={self.room_last_modified_at})>'
        )
