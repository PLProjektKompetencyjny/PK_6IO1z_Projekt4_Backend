from dataclasses import dataclass
from datetime import datetime

from src.utils.utils import db


@dataclass
class ServiceMgmt(db.Model):
    __tablename__ = 'service_mgmt'

    ID: int
    Name: str
    Unit_price: float
    Last_Modified_by: int
    Last_Modified_at: datetime

    ID = db.Column('ID', db.Integer, primary_key=True)
    Name = db.Column('Name', db.String)
    Unit_price = db.Column('unit_price', db.Float)
    Last_Modified_by = db.Column('Last_Modified_by', db.String)
    Last_Modified_at = db.Column('Last_Modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<ServiceMgmt(ID={self.ID}, '
            f'Name={self.Name}, '
            f'Unit_price={self.Unit_price}, '
            f'Last_Modified_by={self.Last_Modified_by}, '
            f'Last_Modified_at={self.Last_Modified_at}>'
        )
