from dataclasses import dataclass, asdict

from src.utils.utils import db


@dataclass
class RoomView(db.Model):
    __tablename__ = 'room_view'

    room_id: int
    room_status_id: int
    room_number_of_single_beds: int
    room_number_of_double_beds: int
    room_number_of_child_beds: int
    room_gross_price: float
    room_gross_price_adult: float
    room_gross_price_child: float
    room_photos_dir: str
    room_last_modified_by: str
    room_last_modified_at: str

    room_id = db.Column('room_id', db.Integer, primary_key=True)
    room_status_id = db.Column('room_status_id', db.Integer)
    room_number_of_single_beds = db.Column('room_number_of_single_beds', db.Integer)
    room_number_of_double_beds = db.Column('room_number_of_double_beds', db.Integer)
    room_number_of_child_beds = db.Column('room_number_of_child_beds', db.Integer)
    room_gross_price = db.Column('room_gross_price', db.Float)
    room_gross_price_adult = db.Column('room_gross_price_adult', db.Float)
    room_gross_price_child = db.Column('room_gross_price_child', db.Float)
    room_photos_dir = db.Column('room_photos_dir', db.String)
    room_last_modified_by = db.Column('room_last_modified_by', db.String)
    room_last_modified_at = db.Column('room_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<RoomView(room_id={self.room_id}, '
            f'room_status_id={self.room_status_id}, '
            f'room_number_of_single_beds={self.room_number_of_single_beds}, '
            f'room_number_of_double_beds={self.room_number_of_double_beds}, '
            f'room_number_of_child_beds={self.room_number_of_child_beds}, '
            f'room_gross_price={self.room_gross_price}, '
            f'room_gross_price_adult={self.room_gross_price_adult}, '
            f'room_gross_price_child={self.room_gross_price_child}, '
            f'room_photos_dir={self.room_photos_dir}, '
            f'room_last_modified_by={self.room_last_modified_by}, '
            f'room_last_modified_at={self.room_last_modified_at})>'
        )


def make_dict(tuple_data):
    return dict(
        room_id=tuple_data[0],
        room_status_id=tuple_data[1],
        room_number_of_single_beds=tuple_data[2],
        room_number_of_double_beds=tuple_data[3],
        room_number_of_child_beds=tuple_data[4],
        room_gross_price=tuple_data[5],
        room_gross_price_adult=tuple_data[6],
        room_gross_price_child=tuple_data[7],
        room_photos_dir=tuple_data[8],
        room_last_modified_by=tuple_data[9],
        room_last_modified_at=tuple_data[10]
    )
