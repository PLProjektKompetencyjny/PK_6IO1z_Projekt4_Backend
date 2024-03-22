from src.utils.utils import db


class CustomerView(db.Model):
    __tablename__ = 'customer_view'

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
