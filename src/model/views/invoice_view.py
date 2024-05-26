from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

from dataclasses import dataclass
from datetime import datetime

from src.utils.utils import db


@dataclass
class InvoiceView(db.Model):
    __tablename__ = 'invoice_view'

    invoice_id: int
    invoice_reservation_id: int
    invoice_date: datetime
    invoice_price_gross: float
    invoice_is_paid: bool
    invoice_status_id: int
    invoice_last_modified_by: int
    invoice_last_modified_at: datetime

    invoice_id = db.Column('invoice_id', db.Integer, primary_key=True)
    invoice_reservation_id = db.Column('invoice_reservation_id', db.Integer)
    invoice_date = db.Column('invoice_date', db.DateTime)
    invoice_price_gross = db.Column('invoice_price_gross', db.Float)
    invoice_is_paid = db.Column('invoice_is_paid', db.Boolean)
    invoice_status_id = db.Column('invoice_status_id', db.Integer)
    invoice_last_modified_by = db.Column('invoice_last_modified_by', db.Integer, nullable=True)
    invoice_last_modified_at = db.Column('invoice_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<InvoiceView(invoice_id={self.invoice_id}, '
            f'invoice_reservation_id={self.invoice_reservation_id}, '
            f'invoice_date={self.invoice_date}, '
            f'invoice_price_gross={self.invoice_price_gross}, '
            f'invoice_is_paid={self.invoice_is_paid}, '
            f'invoice_status_id={self.invoice_status_id}, '
            f'invoice_last_modified_by={self.invoice_last_modified_by}, '
            f'invoice_last_modified_at={self.invoice_last_modified_at})>'
        )
