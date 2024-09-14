import requests

from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus

from src.controller.db_handler import DBHandler
from src.model.views.customer_view import CustomerView
from src.utils.utils import db, HTTPResponse, sqlalchemy_error_to_dict

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound


@dataclass
class ReservationView(db.Model):
    __tablename__ = 'reservation_view'

    reservation_id: int
    reservation_customer_id: int
    reservation_status_id: int
    reservation_number_of_adults: int
    reservation_number_of_children: int
    reservation_start_date: datetime
    reservation_end_date: datetime
    reservation_room_id: int
    reservation_room_status_id: int
    reservation_last_modified_by: int
    reservation_last_modified_at: datetime

    reservation_id = db.Column('reservation_id', db.Integer, primary_key=True, autoincrement=True)
    reservation_customer_id = db.Column('reservation_customer_id', db.Integer)
    reservation_status_id = db.Column('reservation_status_id', db.Integer)
    reservation_number_of_adults = db.Column('room_number_of_adults', db.Integer)
    reservation_number_of_children = db.Column('room_number_of_children', db.Integer)
    reservation_start_date = db.Column('reservation_start_date', db.DateTime)
    reservation_end_date = db.Column('reservation_end_date', db.DateTime)
    reservation_room_id = db.Column('reservation_room_id', db.Integer, primary_key=True)
    reservation_room_status_id = db.Column('reservation_room_status_id', db.Integer)
    reservation_last_modified_by = db.Column('reservation_last_modified_by', db.String)
    reservation_last_modified_at = db.Column('reservation_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<ReservationView(reservation_id={self.reservation_id}, '
            f'reservation_customer_id={self.reservation_customer_id}, '
            f'reservation_status_id={self.reservation_status_id}, '
            f'reservation_number_of_adults={self.reservation_number_of_adults}, '
            f'reservation_number_of_children={self.reservation_number_of_children}, '
            f'reservation_start_date={self.reservation_start_date}, '
            f'reservation_end_date={self.reservation_end_date}, '
            f'reservation_room_id={self.reservation_room_id}, '
            f'reservation_room_status_id={self.reservation_room_status_id}, '
            f'reservation_last_modified_by={self.reservation_last_modified_by}, '
            f'reservation_last_modified_at={self.reservation_last_modified_at})>'
        )

    @staticmethod
    def add_reservation(reservation_customer_id: int,
                        reservation_number_of_adults: int,
                        reservation_number_of_children: int,
                        reservation_room_id: int,
                        reservation_start_date: str,
                        reservation_end_date: str) -> HTTPResponse:
        reservation_start_date = datetime.strptime(reservation_start_date, '%d-%m-%Y')
        reservation_end_date = datetime.strptime(reservation_end_date, '%d-%m-%Y')

        sql = (
            f"""    
            INSERT INTO reservation_view (
                reservation_customer_id, 
                room_number_of_adults, 
                room_number_of_children, 
                reservation_start_date, 
                reservation_end_date, 
                reservation_room_id
            )
            VALUES (
                {reservation_customer_id}, 
                {reservation_number_of_adults}, 
                {reservation_number_of_children}, 
                '{reservation_start_date.strftime('%Y-%m-%d 15:00:00')}', 
                '{reservation_end_date.strftime('%Y-%m-%d 12:00:00')}', 
                {reservation_room_id}
            );

            SELECT MAX(reservation_id) FROM reservation_view;
            """
        )

        return DBHandler.run_sql_query_scalar(sql, 'reservation_id')

    @staticmethod
    def update_reservation(reservation_id: int,
                           reservation_status_id: int,
                           reservation_number_of_adults: int,
                           reservation_number_of_children: int,
                           reservation_start_date: str,
                           reservation_end_date: str,
                           reservation_room_id: int,
                           reservation_room_status_id: int) -> HTTPResponse:

        reservation_start_date = datetime.strptime(reservation_start_date, '%d-%m-%Y')
        reservation_end_date = datetime.strptime(reservation_end_date, '%d-%m-%Y')

        sql = (
            f"""
            UPDATE reservation_view
            SET 
                reservation_status_id = {reservation_status_id},
                room_number_of_adults = {reservation_number_of_adults},
                room_number_of_children = {reservation_number_of_children},
                reservation_start_date = '{reservation_start_date.strftime('%Y-%m-%d 15:00:00')}',
                reservation_end_date = '{reservation_end_date.strftime('%Y-%m-%d 12:00:00')}',
                reservation_room_status_id = {reservation_room_status_id}
            WHERE 
                reservation_id = {reservation_id}
                AND reservation_room_id = {reservation_room_id};
            """
        )

        return DBHandler.run_sql_query(sql)

    @staticmethod
    def delete_reservation(reservation_id: int, reservation_room_id: int) -> HTTPResponse:
        sql = (
            f"""
            DELETE FROM 
                reservation_view
            WHERE 
                reservation_id = {reservation_id}
                AND reservation_room_id = {reservation_room_id};
            """
        )

        return DBHandler.run_sql_query(sql)

    def get_customer_id_from_reservation_id(reservation_id: int, logger):
        try:
            customer_id = db.session.query(
                ReservationView.reservation_customer_id
            ).filter(
                ReservationView.reservation_id == reservation_id
            ).first()
        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            raise e

        if customer_id is None:
            raise NoResultFound

        return customer_id

    @staticmethod
    def get_non_paid_reservations(logger):
        try:
            reservations = db.session.query(
                ReservationView.reservation_id.label('reservation_id'),
                ReservationView.reservation_status_id.label('reservation_status_id')
            ).filter(ReservationView.reservation_status_id != 3).group_by(
                ReservationView.reservation_id,
                ReservationView.reservation_status_id
            ).group_by(
                ReservationView.reservation_id,
                ReservationView.reservation_status_id
            ).all()
            return reservations

        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            raise e

    @staticmethod
    def get_details_for_invoice_about_reservation(reservation_id: int, logger):
        try:
            rows = db.session.query(
                ReservationView.reservation_room_id.label('room_id'),
                ReservationView.reservation_number_of_adults.label('number_of_adults'),
                ReservationView.reservation_number_of_children.label('number_of_children'),
                (ReservationView.reservation_end_date - ReservationView.reservation_start_date).label('duration'),
            ).filter(
                ReservationView.reservation_id == reservation_id
            ).order_by(ReservationView.reservation_room_id
                       ).all()
        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            raise e

        if rows is None:
            raise NoResultFound

        return rows

    @staticmethod
    def set_reservation_as_paid(reservation_id: id):
        sql = (
            f"""
                    UPDATE reservation_view
                    SET 
                        reservation_status_id = 3
                    WHERE 
                        reservation_id = {reservation_id};
                    """
        )

        result = DBHandler.run_sql_query(sql)

        if result[1] != HTTPStatus.OK:
            return result

        reservation = db.session.query(ReservationView).filter(ReservationView.reservation_id == reservation_id).first()
        customer_email = CustomerView.get_customer_email(reservation.reservation_customer_id)

        params = {
            'data_id': reservation_id,
            'address': customer_email,
            'message_type': 'Payment'
        }
        requests.post('http://localhost:5000/api/mailing/sendmail', params=params)
        
        params['message_type'] = 'Invoice'
        requests.post('http://localhost:5000/api/mailing/sendmail', params=params)

        params['message_type'] = 'Reservation'
        return requests.post('http://localhost:5000/api/mailing/sendmail', params=params)
