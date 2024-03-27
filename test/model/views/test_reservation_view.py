from datetime import datetime, timedelta

from src.model.views.reservation_view import ReservationView
from src.utils.utils import db
from test import BaseTestCase


class TestReservationView(BaseTestCase):
    def test_reservation_view_repr(self):
        reservation = ReservationView(
            reservation_id=1,
            reservation_customer_id=1,
            reservation_status_id=1,
            reservation_number_of_adults=2,
            reservation_number_of_children=1,
            reservation_start_date=datetime.now(),
            reservation_end_date=datetime.now() + timedelta(days=7),
            reservation_price_gross=100.0,
            reservation_is_paid=True,
            reservation_room_id=1,
            reservation_room_status_id=1,
            reservation_last_modified_by='John Doe',
            reservation_last_modified_at=datetime.now()
        )
        db.session.add(reservation)
        db.session.commit()

        reservation_from_db = ReservationView.query.get(1)

        self.assertEqual(reservation.reservation_id, reservation_from_db.reservation_id)
        self.assertEqual(reservation.reservation_customer_id, reservation_from_db.reservation_customer_id)
        self.assertEqual(reservation.reservation_status_id, reservation_from_db.reservation_status_id)
        self.assertEqual(reservation.reservation_number_of_adults, reservation_from_db.reservation_number_of_adults)
        self.assertEqual(reservation.reservation_number_of_children, reservation_from_db.reservation_number_of_children)
        self.assertEqual(reservation.reservation_start_date, reservation_from_db.reservation_start_date)
        self.assertEqual(reservation.reservation_end_date, reservation_from_db.reservation_end_date)
        self.assertEqual(reservation.reservation_price_gross, reservation_from_db.reservation_price_gross)
        self.assertEqual(reservation.reservation_is_paid, reservation_from_db.reservation_is_paid)
        self.assertEqual(reservation.reservation_room_id, reservation_from_db.reservation_room_id)
        self.assertEqual(reservation.reservation_room_status_id, reservation_from_db.reservation_room_status_id)
        self.assertEqual(reservation.reservation_last_modified_by, reservation_from_db.reservation_last_modified_by)
        self.assertEqual(reservation.reservation_last_modified_at, reservation_from_db.reservation_last_modified_at)

        self.assertEqual(
            repr(reservation),
            f'<ReservationView(reservation_id={reservation.reservation_id}, '
            f'reservation_customer_id={reservation.reservation_customer_id}, '
            f'reservation_status_id={reservation.reservation_status_id}, '
            f'reservation_number_of_adults={reservation.reservation_number_of_adults}, '
            f'reservation_number_of_children={reservation.reservation_number_of_children}, '
            f'reservation_start_date={reservation.reservation_start_date}, '
            f'reservation_end_date={reservation.reservation_end_date}, '
            f'reservation_price_gross={reservation.reservation_price_gross}, '
            f'reservation_is_paid={reservation.reservation_is_paid}, '
            f'reservation_room_id={reservation.reservation_room_id}, '
            f'reservation_room_status_id={reservation.reservation_room_status_id}, '
            f'reservation_last_modified_by={reservation.reservation_last_modified_by}, '
            f'reservation_last_modified_at={reservation.reservation_last_modified_at})>'
        )