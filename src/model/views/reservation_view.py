from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from src.utils.utils import db
from src.model.views.room_view import RoomView
from src.utils.utils import sqlalchemy_error_to_dict


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
    def get_details_for_invoice_about_reservation(reservation_id: id, logger):
        try:
            rows = db.session.query(
                ReservationView.reservation_id.label('reservation_id'),
                ReservationView.reservation_room_id.label('room_id'),
                ReservationView.reservation_number_of_adults.label('number_of_adults'),
                ReservationView.reservation_number_of_children.label('number_of_children'),
                (ReservationView.reservation_end_date - ReservationView.reservation_start_date).label('duration'),
                (
                        RoomView.room_gross_price +
                        (RoomView.room_gross_price_adult * ReservationView.reservation_number_of_adults) +
                        (RoomView.room_gross_price_child * ReservationView.reservation_number_of_children)
                ).label('gross_price_room')
            ).join(
                RoomView,
                onclause=RoomView.room_id == ReservationView.reservation_room_id
            ).filter(
                ReservationView.reservation_id == reservation_id
            ).all()
        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            raise e

        return rows