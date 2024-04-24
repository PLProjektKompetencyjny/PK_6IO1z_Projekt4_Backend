from datetime import datetime

from src.model.views.user_view import UserView
from test import BaseTestCase


class TestUserView(BaseTestCase):
    def test_user_view(self):
        user = UserView(
            user_id=3,
            user_e_mail='THREE@wp.pl',
            user_name='aaaThree',
            user_is_active=True,
            user_is_admin=False,
            user_last_modified_by=None,
            user_last_modified_at=datetime.fromisoformat('2024-04-23 18:33:36.502758')
        )

        user_from_db = UserView.query.get(3)

        self.assertEqual(user.user_id, user_from_db.user_id)
        self.assertEqual(user.user_e_mail, user_from_db.user_e_mail)
        self.assertEqual(user.user_name, user_from_db.user_name)
        self.assertEqual(user.user_is_active, user_from_db.user_is_active)
        self.assertEqual(user.user_is_admin, user_from_db.user_is_admin)
        self.assertEqual(user.user_last_modified_by, user_from_db.user_last_modified_by)
        self.assertEqual(user.user_last_modified_at, user_from_db.user_last_modified_at)

        self.assertEqual(
            repr(user),
            f'<UserView(user_id={user_from_db.user_id}, '
            f'user_e_mail={user_from_db.user_e_mail}, '
            f'user_name={user_from_db.user_name}, '
            f'user_is_active={user_from_db.user_is_active}, '
            f'user_is_admin={user_from_db.user_is_admin}, '
            f'user_last_modified_by={user_from_db.user_last_modified_by}, '
            f'user_last_modified_at={user_from_db.user_last_modified_at})>'
        )
