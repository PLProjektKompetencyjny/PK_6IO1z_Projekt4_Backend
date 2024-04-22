from src.model.views.user_view import UserView
from src.utils.utils import db
from test import BaseTestCase


class TestUserView(BaseTestCase):
    def test_user_view_repr(self):
        user = UserView(
            user_id=1,
            user_e_mail='john.doe@example.com',
            user_name='John Doe',
            user_password='password',
            user_is_active=True,
            user_is_admin=False,
            user_last_modified_by='John Doe',
            user_last_modified_at='2022-01-01 00:00:00'
        )
        db.session.add(user)
        db.session.commit()

        user_from_db = UserView.query.get(1)

        self.assertEqual(user.user_id, user_from_db.user_id)
        self.assertEqual(user.user_e_mail, user_from_db.user_e_mail)
        self.assertEqual(user.user_name, user_from_db.user_name)
        self.assertEqual(user.user_password, user_from_db.user_password)
        self.assertEqual(user.user_is_active, user_from_db.user_is_active)
        self.assertEqual(user.user_is_admin, user_from_db.user_is_admin)
        self.assertEqual(user.user_last_modified_by, user_from_db.user_last_modified_by)
        self.assertEqual(user.user_last_modified_at, user_from_db.user_last_modified_at)

        self.assertEqual(
            repr(user),
            f'<UserView(user_id={user.user_id}, '
            f'user_e_mail={user.user_e_mail}, '
            f'user_name={user.user_name}, '
            f'user_password={user.user_password}, '
            f'user_is_active={user.user_is_active}, '
            f'user_is_admin={user.user_is_admin}, '
            f'user_last_modified_by={user.user_last_modified_by}, '
            f'user_last_modified_at={user.user_last_modified_at})>'
        )
