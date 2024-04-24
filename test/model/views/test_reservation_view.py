from datetime import datetime

from src.model.views.reservation_view import ReservationView
from test import BaseTestCase


class TestReservationView(BaseTestCase):
    def test_reservation_view(self):
        reservation = ReservationView(
            reservation_id=2,
            reservation_customer_id=2,
            reservation_status_id=1,
            reservation_number_of_adults=1,
            reservation_number_of_children=1,
            reservation_start_date=datetime.fromisoformat('2025-03-03 00:00:00'),
            reservation_end_date=datetime.fromisoformat('2025-03-20 00:00:00'),
            reservation_room_id=2,
            reservation_room_status_id=1,
            reservation_last_modified_by=None,
            reservation_last_modified_at=datetime.fromisoformat('2024-04-23 18:33:36.899953')
        )

        reservation_from_db = ReservationView.query.get(2)

        self.assertEqual(reservation.reservation_id, reservation_from_db.reservation_id)
        self.assertEqual(reservation.reservation_customer_id, reservation_from_db.reservation_customer_id)
        self.assertEqual(reservation.reservation_status_id, reservation_from_db.reservation_status_id)
        self.assertEqual(reservation.reservation_number_of_adults, reservation_from_db.reservation_number_of_adults)
        self.assertEqual(reservation.reservation_number_of_children, reservation_from_db.reservation_number_of_children)
        self.assertEqual(reservation.reservation_start_date, reservation_from_db.reservation_start_date)
        self.assertEqual(reservation.reservation_end_date, reservation_from_db.reservation_end_date)
        self.assertEqual(reservation.reservation_room_id, reservation_from_db.reservation_room_id)
        self.assertEqual(reservation.reservation_room_status_id, reservation_from_db.reservation_room_status_id)
        self.assertEqual(reservation.reservation_last_modified_by, reservation_from_db.reservation_last_modified_by)
        self.assertEqual(reservation.reservation_last_modified_at, reservation_from_db.reservation_last_modified_at)


        self.assertEqual(
            repr(reservation),
            f'<ReservationView(reservation_id={reservation_from_db.reservation_id}, '
            f'reservation_customer_id={reservation_from_db.reservation_customer_id}, '
            f'reservation_status_id={reservation_from_db.reservation_status_id}, '
            f'reservation_number_of_adults={reservation_from_db.reservation_number_of_adults}, '
            f'reservation_number_of_children={reservation_from_db.reservation_number_of_children}, '
            f'reservation_start_date={reservation_from_db.reservation_start_date}, '
            f'reservation_end_date={reservation_from_db.reservation_end_date}, '
            f'reservation_room_id={reservation_from_db.reservation_room_id}, '
            f'reservation_room_status_id={reservation_from_db.reservation_room_status_id}, '
            f'reservation_last_modified_by={reservation_from_db.reservation_last_modified_by}, '
            f'reservation_last_modified_at={reservation_from_db.reservation_last_modified_at})>'
        )
