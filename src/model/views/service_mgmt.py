from dataclasses import dataclass
from datetime import datetime

from src.controller.db_handler import DBHandler
from src.utils.utils import db, HTTPResponse


@dataclass
class ServiceMgmt(db.Model):
    __tablename__ = 'service_mgmt'

    id: int
    name: str
    unit_price: float
    last_modified_by: int
    last_modified_at: datetime

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    unit_price = db.Column('unit_price', db.Float)
    last_modified_by = db.Column('last_modified_by', db.String)
    last_modified_at = db.Column('last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<ServiceMgmt(id={self.id}, '
            f'name={self.name}, '
            f'unit_price={self.unit_price}, '
            f'last_modified_by={self.last_modified_by}, '
            f'last_modified_at={self.last_modified_at}>'
        )

    @staticmethod
    def add_service(name: str, unit_price: float) -> HTTPResponse:
        sql = (
            f"""
            INSERT INTO service_mgmt (
                id,
                name, 
                unit_price 
            )
            VALUES (
                nextval('service_id_seq'),
                '{name}',
                {unit_price}
            );
            
            SELECT MAX(id) FROM service_mgmt;
            """
        )

        return DBHandler.run_sql_query_scalar(sql, 'service_id')

    @staticmethod
    def update_service(id: int, name: str, unit_price: float):
        sql = (
            f"""
            UPDATE 
                service_mgmt
            SET
                name = '{name}',
                unit_price = {unit_price}
            WHERE
                id = {id}
            """
        )

        return DBHandler.run_sql_query(sql)
