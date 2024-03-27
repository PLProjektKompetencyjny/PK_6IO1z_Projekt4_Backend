from src.utils.utils import db


class ReservationView(db.Model):
    __tablename__ = 'reservation_view'

    reservation_id: int
    reservation_customer_id: int
    reservation_status_id: int
    reservation_number_of_adults: int
    reservation_number_of_children: int
    reservation_start_date: str
    reservation_end_date: str
    reservation_price_gross: float
    reservation_is_paid: bool
    reservation_room_id: int
    reservation_room_status_id: int
    reservation_last_modified_by: str
    reservation_last_modified_at: str

    reservation_id = db.Column('reservation_id', db.Integer, primary_key=True)
    reservation_customer_id = db.Column('reservation_customer_id', db.Integer)
    reservation_status_id = db.Column('reservation_status_id', db.Integer)
    reservation_number_of_adults = db.Column('reservation_number_of_adults', db.Integer)
    reservation_number_of_children = db.Column('reservation_number_of_children', db.Integer)
    reservation_start_date = db.Column('reservation_start_date', db.DateTime)
    reservation_end_date = db.Column('reservation_end_date', db.DateTime)
    reservation_price_gross = db.Column('reservation_price_gross', db.Float)
    reservation_is_paid = db.Column('reservation_is_paid', db.Boolean)
    reservation_room_id = db.Column('reservation_room_id', db.Integer)
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
            f'reservation_price_gross={self.reservation_price_gross}, '
            f'reservation_is_paid={self.reservation_is_paid}, '
            f'reservation_room_id={self.reservation_room_id}, '
            f'reservation_room_status_id={self.reservation_room_status_id}, '
            f'reservation_last_modified_by={self.reservation_last_modified_by}, '
            f'reservation_last_modified_at={self.reservation_last_modified_at})>'
        )
