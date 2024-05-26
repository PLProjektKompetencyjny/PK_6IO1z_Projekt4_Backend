from datetime import datetime

from src.model.views.room_view import RoomView
from test import BaseTestCase


class TestRoomView(BaseTestCase):
    def test_room_view(self):
        room = RoomView(
            room_id=1,
            room_type_id=1,
            room_status_id=1,
            room_number_of_single_beds=0,
            room_number_of_double_beds=1,
            room_number_of_child_beds=1,
            room_gross_price=10.0,
            room_gross_price_adult=20.0,
            room_gross_price_child=10.0,
            room_photos_dir='/',
            room_last_modified_by=None,
            room_last_modified_at=datetime.fromisoformat('2024-04-23 18:33:36.518408')
        )

        room_from_db = RoomView.query.get(1)

        self.assertEqual(room.room_id, room_from_db.room_id)
        self.assertEqual(room.room_type_id, room_from_db.room_type_id)
        self.assertEqual(room.room_status_id, room_from_db.room_status_id)
        self.assertEqual(room.room_number_of_single_beds, room_from_db.room_number_of_single_beds)
        self.assertEqual(room.room_number_of_double_beds, room_from_db.room_number_of_double_beds)
        self.assertEqual(room.room_number_of_child_beds, room_from_db.room_number_of_child_beds)
        self.assertEqual(room.room_gross_price, room_from_db.room_gross_price)
        self.assertEqual(room.room_gross_price_adult, room_from_db.room_gross_price_adult)
        self.assertEqual(room.room_gross_price_child, room_from_db.room_gross_price_child)
        self.assertEqual(room.room_photos_dir, room_from_db.room_photos_dir)
        self.assertEqual(room.room_last_modified_by, room_from_db.room_last_modified_by)
        self.assertEqual(room.room_last_modified_at, room_from_db.room_last_modified_at)

        self.assertEqual(
            repr(room),
            f'<RoomView(room_id={room_from_db.room_id}, '
            f'room_type_id={room_from_db.room_type_id}, '
            f'room_status_id={room_from_db.room_status_id}, '
            f'room_number_of_single_beds={room_from_db.room_number_of_single_beds}, '
            f'room_number_of_double_beds={room_from_db.room_number_of_double_beds}, '
            f'room_number_of_child_beds={room_from_db.room_number_of_child_beds}, '
            f'room_gross_price={room_from_db.room_gross_price}, '
            f'room_gross_price_adult={room_from_db.room_gross_price_adult}, '
            f'room_gross_price_child={room_from_db.room_gross_price_child}, '
            f'room_photos_dir={room_from_db.room_photos_dir}, '
            f'room_last_modified_by={room_from_db.room_last_modified_by}, '
            f'room_last_modified_at={room_from_db.room_last_modified_at})>'
        )
