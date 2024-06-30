from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from src.controller.types.response import Response
from src.controller.db_handler import DBHandler
from src.utils.utils import db, HTTPResponse, sqlalchemy_error_to_dict

from sqlalchemy.exc import SQLAlchemyError


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
    def add_customer(
        customer_email: str,
        customer_nip_number: None,
        customer_name: str,
        customer_surname: str,
        customer_phone: str,
        customer_city: str,
        customer_postal_code: str,
        customer_street: str,
        customer_building_number: str,
        customer_last_modified_by: None, ) -> HTTPResponse:
        new_user_id = db.session.query(
            func.insert_user_account(customer_email, '', None)
        ).scalar()

        sql = (
            f"""    
            INSERT INTO customer_view(
                customer_id,
                customer_email,
                customer_nip_number,
                customer_name,
                customer_surname,
                customer_phone,
                customer_city,
                customer_postal_code,
                customer_street,
                customer_building_number,
                customer_last_modified_by)
            VALUES(
                {new_user_id},
                '{customer_email}',
                {'NULL' if customer_nip_number is None else f"'{customer_nip_number}'"},
                '{customer_name}',
                '{customer_surname}',
                '{customer_phone}',
                '{customer_city}',
                '{customer_postal_code}',
                '{customer_street}',
                '{customer_building_number}',
                {'NULL' if customer_last_modified_by is None else f"'{customer_last_modified_by}'"}
            );

            SELECT MAX(customer_id) FROM customer_view;
            """
        )

        return DBHandler.run_sql_query_scalar(sql, 'customer_id')

    @staticmethod
    def update_customer(customer_id: int,
                        customer_email: str,
                        customer_nip_number: None,
                        customer_name: str,
                        customer_surname: str,
                        customer_phone: str,
                        customer_city: str,
                        customer_postal_code: str,
                        customer_street: str,
                        customer_building_number: str,
                        customer_last_modified_by: None, ) -> HTTPResponse:
        sql = (
            f"""    
            UPDATE customer_view
            SET
                customer_email = '{customer_email}',
                customer_nip_number = {'NULL' if customer_nip_number is None else f"'{customer_nip_number}'"},
                customer_name = '{customer_name}',
                customer_surname = '{customer_surname}',
                customer_phone = '{customer_phone}',
                customer_city = '{customer_city}',
                customer_postal_code = '{customer_postal_code}',
                customer_street = '{customer_street}',
                customer_building_number = '{customer_building_number}',
                customer_last_modified_by = {'NULL' if customer_last_modified_by is None else f"'{customer_last_modified_by}'"}
            WHERE 
                customer_id = {customer_id}
            """
        )

        return DBHandler.run_sql_query(sql)

    def get_customer_details_by_id(customer_id: int, logger):
        try:
            rows = (db.session.query(
                CustomerView
            ).filter(
                CustomerView.customer_id == customer_id
            ).first())
        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            raise e

        if rows is None:
            raise NoResultFound

        return rows
