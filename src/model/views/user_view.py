from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus

from sqlalchemy import func

from src.controller.types.response import Response
from src.controller.db_handler import DBHandler
from src.utils.utils import db


@dataclass
class UserView(db.Model):
    __tablename__ = 'user_view'

    user_id: int
    user_e_mail: str
    user_name: str
    user_is_active: bool
    user_is_admin: bool
    user_last_modified_by: int
    user_last_modified_at: datetime

    user_id = db.Column('user_id', db.Integer, primary_key=True)
    user_e_mail = db.Column('user_e_mail', db.String)
    user_name = db.Column('user_name', db.String)
    user_is_active = db.Column('user_is_active', db.Boolean)
    user_is_admin = db.Column('user_is_admin', db.Boolean)
    user_last_modified_by = db.Column('user_last_modified_by', db.String)
    user_last_modified_at = db.Column('user_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<UserView(user_id={self.user_id}, '
            f'user_e_mail={self.user_e_mail}, '
            f'user_name={self.user_name}, '
            f'user_is_active={self.user_is_active}, '
            f'user_is_admin={self.user_is_admin}, '
            f'user_last_modified_by={self.user_last_modified_by}, '
            f'user_last_modified_at={self.user_last_modified_at})>'
        )

    @staticmethod
    def add_user(login: str,
                 user_password: str,
                 last_modified_by_id: int = None) -> tuple[Response, HTTPStatus]:
        return DBHandler.run_sql_function_scalar(
            func.insert_user_account, login, user_password, last_modified_by_id
        )

    @staticmethod
    def update_user_password(login: str, new_user_password: str,
                             old_user_password: str,
                             last_modified_by_id: int = None) -> tuple[Response, HTTPStatus]:
        return DBHandler.run_sql_function_scalar(
            func.update_user_account_password, login, new_user_password, old_user_password, last_modified_by_id
        )

    @staticmethod
    def authenticate_user(login: str,
                          user_password: str) -> tuple[Response, HTTPStatus]:
        return DBHandler.run_sql_function_scalar(
            func.authenticate_user_account, login, user_password
        )

    @staticmethod
    def insert_user_account(login: str, user_password: str, last_modified_by_id: int = None) -> int:
        id_to_return = None
        try:
            id_to_return = (
                db
                .session
                .query(
                    func
                    .insert_user_account(login, user_password, last_modified_by_id)
                )
                .scalar()
            )
            (
                db
                .session
                .commit()
            )
        except:
            id_to_return = None
            (
                db
                .session
                .rollback()
            )

        return id_to_return

    @staticmethod
    def update_user_account_password(login: str, new_user_password: str, old_user_password: str,
                                     last_modified_by_id: int = None) -> int:
        id_to_return = None
        try:
            id_to_return = (
                db
                .session
                .query(
                    func
                    .update_user_account_password(login, new_user_password, old_user_password, last_modified_by_id)
                )
                .scalar()
            )
            (
                db
                .session
                .commit()
            )
        except:
            id_to_return = None
            (
                db
                .session
                .rollback()
            )

        return id_to_return

    @staticmethod
    def authenticate_user_account(login: str, user_password: str) -> int:
        try:
            return (
                db
                .session
                .query(
                    func
                    .authenticate_user_account(login, user_password)
                )
                .scalar()
            )
        except:
            (
                db
                .session
                .rollback()
            )
            return None
