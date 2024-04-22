from src.model.views.customer_view import CustomerView
from src.utils.utils import db
from test import BaseTestCase


class TestCustomerView(BaseTestCase):
    def test_customer_view_repr(self):
        customer = CustomerView(
            customer_id=1,
            customer_nip_number='1234567890',
            customer_name='John',
            customer_surname='Doe',
            customer_email='john.doe@example.com',
            customer_phone='123456789',
            customer_city='City',
            customer_postal_code='12345',
            customer_street='Street',
            customer_building_number='1',
            customer_last_modified_by='John Doe',
            customer_last_modified_at='2022-01-01 00:00:00'
        )
        db.session.add(customer)
        db.session.commit()

        customer_from_db = CustomerView.query.get(1)

        self.assertEqual(customer.customer_id, customer_from_db.customer_id)
        self.assertEqual(customer.customer_nip_number, customer_from_db.customer_nip_number)
        self.assertEqual(customer.customer_name, customer_from_db.customer_name)
        self.assertEqual(customer.customer_surname, customer_from_db.customer_surname)
        self.assertEqual(customer.customer_email, customer_from_db.customer_email)
        self.assertEqual(customer.customer_phone, customer_from_db.customer_phone)
        self.assertEqual(customer.customer_city, customer_from_db.customer_city)
        self.assertEqual(customer.customer_postal_code, customer_from_db.customer_postal_code)
        self.assertEqual(customer.customer_street, customer_from_db.customer_street)
        self.assertEqual(customer.customer_building_number, customer_from_db.customer_building_number)
        self.assertEqual(customer.customer_last_modified_by, customer_from_db.customer_last_modified_by)
        self.assertEqual(customer.customer_last_modified_at, customer_from_db.customer_last_modified_at)

        self.assertEqual(
            repr(customer),
            f'<CustomerView(customer_id={customer.customer_id}, '
            f'customer_nip_number={customer.customer_nip_number}, '
            f'customer_name={customer.customer_name}, '
            f'customer_surname={customer.customer_surname}, '
            f'customer_email={customer.customer_email}, '
            f'customer_phone={customer.customer_phone}, '
            f'customer_city={customer.customer_city}, '
            f'customer_postal_code={customer.customer_postal_code}, '
            f'customer_street={customer.customer_street}, '
            f'customer_building_number={customer.customer_building_number}, '
            f'customer_last_modified_by={customer.customer_last_modified_by}, '
            f'customer_last_modified_at={customer.customer_last_modified_at})>'
        )
