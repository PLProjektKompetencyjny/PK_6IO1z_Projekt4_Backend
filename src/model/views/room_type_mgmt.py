from dataclasses import dataclass
from datetime import datetime

from src.utils.utils import db


@dataclass
class RoomTypeMgmt(db.Model):
    __tablename__ = 'room_type_mgmt'

    ID: int
    num_of_single_beds: int
    num_of_double_beds: int
    num_of_child_beds: int
    adult_price_gross: float
    child_price_gross: float
    photos_dir: str
    last_Modified_by: int
    last_Modified_at: datetime

    ID = db.Column('id', db.Integer, primary_key=True)
    num_of_single_beds = db.Column('num_of_single_beds', db.Integer)
    num_of_double_beds = db.Column('num_of_double_beds', db.Integer)
    num_of_child_beds = db.Column('num_of_child_beds', db.Integer)
    adult_price_gross = db.Column('adult_price_gross', db.Float)
    child_price_gross = db.Column('child_price_gross', db.Float)
    photos_dir = db.Column('photos_dir', db.String)
    last_Modified_by = db.Column('last_modified_by', db.String)
    last_Modified_at = db.Column('last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<RoomTypeMgmt(ID={self.ID}, '
            f'Num_of_single_beds={self.num_of_single_beds}, '
            f'Num_of_double_beds={self.num_of_double_beds}, '
            f'Num_of_child_beds={self.num_of_child_beds}, '
            f'Adult_price_gross={self.adult_price_gross}, '
            f'Child_price_gross={self.child_price_gross}, '
            f'Photos_dir={self.photos_dir}, '
            f'Last_Modified_by={self.last_Modified_by}, '
            f'Last_Modified_at={self.last_Modified_at}>'
        )
