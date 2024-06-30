from dataclasses import dataclass
from datetime import datetime

from src.utils.utils import db


@dataclass
class ServiceMgmt(db.Model):
    __tablename__ = 'service_mgmt'

    id: int
    name: str
    unit_price: float
    last_modified_by: int
    last_modified_at: datetime

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    unit_price = db.Column('unit_price', db.Float)
    last_modified_by = db.Column('last_modified_by', db.String)
    last_modified_at = db.Column('last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<ServiceMgmt(id={self.id}, '
            f'name={self.name}, '
            f'unit_price={self.unit_price}, '
            f'last_modified_by={self.last_modified_by}, '
            f'last_modified_at={self.last_modified_at}>'
        )
