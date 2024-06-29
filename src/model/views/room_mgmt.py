from dataclasses import dataclass
from datetime import datetime

from src.utils.utils import db


@dataclass
class RoomMgmt(db.Model):
    __tablename__ = 'room_mgmt'

    id: int
    room_type_id: int
    status_id: int
    room_price_gross: float
    last_modified_by: int
    last_modified_at: datetime

    id = db.Column('id', db.Integer, primary_key=True)
    room_type_id = db.Column('room_type_id', db.Integer)
    status_id = db.Column('status_id', db.Integer)
    room_price_gross = db.Column('room_price_gross', db.Float)
    last_modified_by = db.Column('last_modified_by', db.String)
    last_modified_at = db.Column('last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<RoomMgmt(id={self.id}, '
            f'room_type_id={self.room_type_id}, '
            f'status_id={self.status_id}, '
            f'room_price_gross={self.room_price_gross}, '
            f'last_modified_by={self.last_modified_by}, '
            f'last_modified_at={self.last_modified_at}>'
        )
