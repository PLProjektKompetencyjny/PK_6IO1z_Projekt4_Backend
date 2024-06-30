from dataclasses import dataclass
from datetime import datetime

from http import HTTPStatus

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from src.controller.db_handler import DBHandler
from src.model.enums.invoice_status import InvoiceStatus
from src.controller.types.response import Response
from src.utils.utils import db, HTTPResponse, sqlalchemy_error_to_dict

@dataclass
class InvoiceView(db.Model):
    __tablename__ = 'invoice_view'
    
    invoice_id = db.Column('invoice_id', db.Integer, primary_key=True, autoincrement=True)
    invoice_reservation_id = db.Column('invoice_reservation_id', db.Integer, primary_key=True)
    invoice_room_id = db.Column('invoice_room_id', db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column('invoice_id', db.Integer, primary_key=True)
    invoice_reservation_id = db.Column('invoice_reservation_id', db.Integer)
    invoice_room_id = db.Column('invoice_room_id', db.Integer, primary_key=True)
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
        DBHandler.run_sql_function_all(
            func.calculate_invoice_price, reservation_id
        )

    @staticmethod
    def add_invoice(invoice_reservation_id: int) -> HTTPResponse:
        sql = (
            f"""    
            INSERT INTO 
                invoice_view (invoice_reservation_id)
            VALUES 
                ({invoice_reservation_id});
                
            SELECT MAX(invoice_id) FROM invoice_view;
            """
        )

        return DBHandler.run_sql_query_scalar(sql, 'invoice_id')

    @staticmethod
    def update_invoice(invoice_id: int, invoice_status_id: int) -> HTTPResponse:
        if invoice_status_id == InvoiceStatus.PAID.value:
            sql = (
                f"""
                UPDATE invoice_view
                SET 
                    invoice_status_id = {invoice_status_id},
                    invoice_is_paid = TRUE
                WHERE 
                    invoice_id = {invoice_id}
            """
            )
        else:
            sql = (
                f"""
                UPDATE invoice_view
                SET 
                    invoice_status_id = {invoice_status_id}
                WHERE 
                    invoice_id = {invoice_id}
            """
            )

        return DBHandler.run_sql_query(sql)
    
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
    def get_invoice_details_for_single_reservation(reservation_id: int, logger):
        try:
            rows = db.session.query(
                InvoiceView.invoice_date.label('invoice_date'),
                InvoiceView.invoice_id.label('invoice_id'),
                InvoiceView.invoice_price_gross.label('invoice_price_gross')
            ).filter(
                InvoiceView.invoice_reservation_id == reservation_id
            ).first()
        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            raise e

        if rows is None:
            raise NoResultFound

        return rows

    @staticmethod
    def get_rooms_prices_for_reservation(reservation_id: int, logger):
        try:
            rows = db.session.query(
                InvoiceView.invoice_room_price_gross.label('invoice_room_price_gross')
            ).filter(
                InvoiceView.invoice_reservation_id == reservation_id
            ).order_by(
                InvoiceView.invoice_room_id
            ).all()
        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            raise e

        if rows is None:
            raise NoResultFound

        return rows
      
