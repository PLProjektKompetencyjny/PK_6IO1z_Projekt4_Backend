from unittest import TestCase, main

from http import HTTPStatus

from src import create_app
from src.controller.enums.database_response_status import DatabaseResponseStatus


class TestCustomerViewController(TestCase):
    def setUp(self):
        self.app = create_app('test')
        self.client = self.app.test_client()

    def test_get_customers_endpoint(self):
        response = self.client.get('/database/customers')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.OK.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.OK.get_description())

    def test_get_customers_with_filters(self):
        response = self.client.get('/database/customers?customer_id=1')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.OK.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.OK.get_description())

    def test_get_customers_with_invalid_filters(self):
        response = self.client.get('/database/customers?customer_id=>3')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.OK.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.OK.get_description())

    def test_get_customers_with_no_results(self):
        response = self.client.get('/database/customers?customer_id=!1')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.OK.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.OK.get_description())

    def test_get_customers_with_invalid_filter(self):
        response = self.client.get('/database/customers?customer_id=-3')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json["code"], DatabaseResponseStatus.NOT_FOUND.get_value())
        self.assertEqual(response.json["code_message"], DatabaseResponseStatus.NOT_FOUND.get_description())


if __name__ == '__main__':
    main()
