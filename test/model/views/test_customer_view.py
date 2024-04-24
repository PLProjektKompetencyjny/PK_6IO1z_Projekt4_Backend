from datetime import datetime

from src.model.views.customer_view import CustomerView
from test import BaseTestCase


class TestCustomerView(BaseTestCase):
    def test_customer_view(self):
        customer = CustomerView(
            customer_id=3,
            customer_nip_number=None,
            customer_name='THREEaaa',
            customer_surname='THREEbbb',
            customer_email='THREE@wp.pl',
            customer_phone='+48123456789',
            customer_city='GDA',
            customer_postal_code='10-881',
            customer_street='THREEplpl',
            customer_building_number='33',
            customer_last_modified_by=None,
            customer_last_modified_at=datetime.fromisoformat('2024-04-23 18:33:36.510353')
        )

        customer_from_db = CustomerView.query.get(3)

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
            f'<CustomerView(customer_id={customer_from_db.customer_id}, '
            f'customer_nip_number={customer_from_db.customer_nip_number}, '
            f'customer_name={customer_from_db.customer_name}, '
            f'customer_surname={customer_from_db.customer_surname}, '
            f'customer_email={customer_from_db.customer_email}, '
            f'customer_phone={customer_from_db.customer_phone}, '
            f'customer_city={customer_from_db.customer_city}, '
            f'customer_postal_code={customer_from_db.customer_postal_code}, '
            f'customer_street={customer_from_db.customer_street}, '
            f'customer_building_number={customer_from_db.customer_building_number}, '
            f'customer_last_modified_by={customer_from_db.customer_last_modified_by}, '
            f'customer_last_modified_at={customer_from_db.customer_last_modified_at})>'
        )
