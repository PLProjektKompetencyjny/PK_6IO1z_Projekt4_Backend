from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from logging import getLogger

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.controller.enums.database_response_status import DatabaseResponseStatus
from src.controller.types.response import Response
from src.utils.utils import db, sqlalchemy_error_to_dict


@dataclass
class CustomerView(db.Model):
    __tablename__ = 'customer_view'

    customer_id: int
    customer_nip_number: str
    customer_name: str
    customer_surname: str
    customer_email: str
    customer_phone: str
    customer_city: str
    customer_postal_code: str
    customer_street: str
    customer_building_number: str
    customer_last_modified_by: int
    customer_last_modified_at: datetime

    customer_id = db.Column('customer_id', db.Integer, primary_key=True)
    customer_nip_number = db.Column('customer_nip_number', db.String)
    customer_name = db.Column('customer_name', db.String)
    customer_surname = db.Column('customer_surname', db.String)
    customer_email = db.Column('customer_email', db.String)
    customer_phone = db.Column('customer_phone', db.String)
    customer_city = db.Column('customer_city', db.String)
    customer_postal_code = db.Column('customer_postal_code', db.String)
    customer_street = db.Column('customer_street', db.String)
    customer_building_number = db.Column('customer_building_number', db.String)
    customer_last_modified_by = db.Column('customer_last_modified_by', db.String)
    customer_last_modified_at = db.Column('customer_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<CustomerView(customer_id={self.customer_id}, '
            f'customer_nip_number={self.customer_nip_number}, '
            f'customer_name={self.customer_name}, '
            f'customer_surname={self.customer_surname}, '
            f'customer_email={self.customer_email}, '
            f'customer_phone={self.customer_phone}, '
            f'customer_city={self.customer_city}, '
            f'customer_postal_code={self.customer_postal_code}, '
            f'customer_street={self.customer_street}, '
            f'customer_building_number={self.customer_building_number}, '
            f'customer_last_modified_by={self.customer_last_modified_by}, '
            f'customer_last_modified_at={self.customer_last_modified_at})>'
        )

    @staticmethod
    def update_customer(customer_id: int,
                        customer_nip_number: None,
                        customer_name: str,
                        customer_surname: str,
                        customer_phone: str,
                        customer_city: str,
                        customer_postal_code: str,
                        customer_street: str,
                        customer_building_number: str,
                        customer_last_modified_by: None, ) -> tuple[Response, HTTPStatus]:
        sql = text(
            f"""    
            UPDATE customer_view
            SET
                customer_nip_number = {'NULL' if customer_nip_number is None else f"'{customer_nip_number}'"},
                customer_name = '{customer_name}',
                customer_surname = '{customer_surname}',
                customer_phone = '{customer_phone}',
                customer_city = '{customer_city}',
                customer_postal_code = '{customer_postal_code}',
                customer_street = '{customer_street}',
                customer_building_number = '{customer_building_number}',
                customer_last_modified_by = {'NULL' if customer_last_modified_by is None else f"'{customer_last_modified_by}'"}
            WHERE customer_id = {customer_id}
            """
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
