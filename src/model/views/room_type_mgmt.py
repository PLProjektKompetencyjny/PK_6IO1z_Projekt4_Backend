from dataclasses import dataclass
from datetime import datetime

from src.utils.utils import db


@dataclass
class RoomTypeMgmt(db.Model):
    __tablename__ = 'room_type_mgmt'

    ID: int
    Num_of_single_beds: int
    Num_of_double_beds: int
    Num_of_child_beds: int
    Adult_price_gross: float
    Child_price_gross: float
    Photos_dir: str
    Last_Modified_by: int
    Last_Modified_at: datetime

    ID = db.Column('ID', db.Integer, primary_key=True)
    Num_of_single_beds = db.Column('Name', db.Integer)
    Num_of_double_beds = db.Column('Name', db.Integer)
    Num_of_child_beds = db.Column('Name', db.Integer)
    Adult_price_gross = db.Column('Name', db.Float)
    Child_price_gross = db.Column('Name', db.Float)
    Photos_dir = db.Column('Last_Modified_by', db.String)
    Last_Modified_by = db.Column('Last_Modified_by', db.String)
    Last_Modified_at = db.Column('Last_Modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<RoomTypeMgmt(ID={self.ID}, '
            f'Num_of_single_beds={self.Num_of_single_beds}, '
            f'Num_of_double_beds={self.Num_of_double_beds}, '
            f'Num_of_child_beds={self.Num_of_child_beds}, '
            f'Adult_price_gross={self.Adult_price_gross}, '
            f'Child_price_gross={self.Child_price_gross}, '
            f'Photos_dir={self.Photos_dir}, '
            f'Last_Modified_by={self.Last_Modified_by}, '
            f'Last_Modified_at={self.Last_Modified_at}>'
        )
