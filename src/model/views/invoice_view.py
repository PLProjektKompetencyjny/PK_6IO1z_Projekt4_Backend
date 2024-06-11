from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from logging import getLogger

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, insert

from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.controller.types.response import Response
from src.utils.utils import db, sqlalchemy_error_to_dict
from sqlalchemy import func


@dataclass
class InvoiceView(db.Model):
    __tablename__ = 'invoice_view'

    invoice_id: int
    invoice_reservation_id: int
    invoice_room_id: int
    invoice_room_price_gross: float
    invoice_date: datetime
    invoice_price_gross: float
    invoice_is_paid: bool
    invoice_status_id: int
    invoice_last_modified_by: int
    invoice_last_modified_at: datetime

    invoice_id = db.Column('invoice_id', db.Integer, primary_key=True, autoincrement=True)
    invoice_reservation_id = db.Column('invoice_reservation_id', db.Integer)
    invoice_room_id = db.Column('invoice_room_id', db.Integer)
    invoice_room_price_gross = db.Column('invoice_room_price_gross', db.Float)
    invoice_date = db.Column('invoice_date', db.DateTime)
    invoice_price_gross = db.Column('invoice_price_gross', db.Float)
    invoice_is_paid = db.Column('invoice_is_paid', db.Boolean)
    invoice_status_id = db.Column('invoice_status_id', db.Integer)
    invoice_last_modified_by = db.Column('invoice_last_modified_by', db.Integer)
    invoice_last_modified_at = db.Column('invoice_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<InvoiceView(invoice_id={self.invoice_id}, '
            f'invoice_reservation_id={self.invoice_reservation_id}, '
            f'invoice_room_id={self.invoice_room_id},'
            f'invoice_room_price_gross={self.invoice_room_price_gross},'
            f'invoice_date={self.invoice_date}, '
            f'invoice_is_paid={self.invoice_is_paid},'
            f'invoice_price_gross={self.invoice_price_gross},'
            f'invoice_status_id={self.invoice_status_id}, '
            f'invoice_last_modified_by={self.invoice_last_modified_by}, '
            f'invoice_last_modified_at={self.invoice_last_modified_at})>'
        )

    @staticmethod
    def calculate_invoice_price(reservation_id: int) -> None:
        (
            db
            .session
            .query(
                func
                .calculate_invoice_price(reservation_id)
            )
            .all()
        )
        (
            db
            .session
            .commit()
        )
        return None

    @staticmethod
    def add_invoice(reservation_id: int) -> tuple[Response, HTTPStatus]:
        sql = insert(InvoiceView).values(
            invoice_reservation_id=reservation_id
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
