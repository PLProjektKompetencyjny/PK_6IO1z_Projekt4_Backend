from unittest import main, TestCase

from http import HTTPStatus

from src import create_app
from src.controller.enums.database_response_status import DatabaseResponseStatus


class TestDatabaseBlueprint(TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()

    def test_customers_endpoint(self):
        response = self.client.get('/database/customers')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.OK.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.OK.get_description())

    def test_rooms_endpoint(self):
        response = self.client.get('/database/rooms')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.OK.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.OK.get_description())

    def test_invoices_endpoint(self):
        response = self.client.get('/database/invoices')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.OK.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.OK.get_description())

    def test_users_endpoint(self):
        response = self.client.get('/database/users')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.OK.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.OK.get_description())

    def test_reservations_endpoint(self):
        response = self.client.get('/database/reservations')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.OK.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.OK.get_description())


if __name__ == '__main__':
    main()
