from src.utils.utils import db


class UserView(db.Model):
    __tablename__ = 'user_view'

    user_id: int
    user_e_mail: str
    user_name: str
    user_password: str
    user_is_active: bool
    user_is_admin: bool
    user_last_modified_by: str
    user_last_modified_at: str

    user_id = db.Column('user_id', db.Integer, primary_key=True)
    user_e_mail = db.Column('user_e_mail', db.String)
    user_name = db.Column('user_name', db.String)
    user_password = db.Column('user_password', db.String)
    user_is_active = db.Column('user_is_active', db.Boolean)
    user_is_admin = db.Column('user_is_admin', db.Boolean)
    user_last_modified_by = db.Column('user_last_modified_by', db.String)
    user_last_modified_at = db.Column('user_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<UserView(user_id={self.user_id}, '
            f'user_e_mail={self.user_e_mail}, '
            f'user_name={self.user_name}, '
            f'user_password={self.user_password}, '
            f'user_is_active={self.user_is_active}, '
            f'user_is_admin={self.user_is_admin}, '
            f'user_last_modified_by={self.user_last_modified_by}, '
            f'user_last_modified_at={self.user_last_modified_at})>'
        )
