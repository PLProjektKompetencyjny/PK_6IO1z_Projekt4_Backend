from dataclasses import dataclass
from datetime import datetime

from src.utils.utils import db


@dataclass
class RoomMgmt(db.Model):
    __tablename__ = 'room_mgmt'

    ID: int
    Room_type_ID: int
    Status_ID: int
    Room_price_gross: float
    Last_Modified_by: int
    Last_Modified_at: datetime

    ID = db.Column('ID', db.Integer, primary_key=True)
    Room_type_ID = db.Column('Room_type_ID', db.Integer)
    Status_ID = db.Column('Status_ID', db.Integer)
    Room_price_gross = db.Column('Room_price_gross', db.Float)
    Last_Modified_by = db.Column('Last_Modified_by', db.String)
    Last_Modified_at = db.Column('Last_Modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<RoomMgmt(ID={self.ID}, '
            f'Room_type_ID={self.Room_type_ID}, '
            f'Status_ID={self.Status_ID}, '
            f'Room_price_gross={self.Room_price_gross}, '
            f'Last_Modified_by={self.Last_Modified_by}, '
            f'Last_Modified_at={self.Last_Modified_at}>'
        )
