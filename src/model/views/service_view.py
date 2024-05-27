from dataclasses import dataclass
from datetime import datetime

from src.utils.utils import db


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
