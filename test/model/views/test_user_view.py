from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from src.model.views.user_view import UserView
from src.utils.utils import db
from test import BaseTestCase


class TestUserView(BaseTestCase):
    def test_user_view_insert(self):
        user_name = 'TestUser'
        user_password = 'TestPassword'
        user_last_modified_by = None

        try:
            user_id = db.session.query(
                func.insert_user_account(user_name, user_password, user_last_modified_by)).scalar()
            auth_user_id = db.session.query(func.authenticate_user_account(user_name, user_password)).scalar()
            db.session.commit()

            self.assertEqual(user_id, auth_user_id)
        except SQLAlchemyError as e:
            self.fail(e)
