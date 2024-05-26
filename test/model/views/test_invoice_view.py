from datetime import datetime

from src.model.views.invoice_view import InvoiceView
from test import BaseTestCase


class TestInvoiceView(BaseTestCase):
    def test_invoice_view(self):
        invoice = InvoiceView(
            invoice_id=1,
            invoice_reservation_id=1,
            invoice_date=datetime.fromisoformat('2024-04-23 18:33:36.968453'),
            invoice_price_gross=50.0,
            invoice_is_paid=False,
            invoice_status_id=1,
            invoice_last_modified_by=None,
            invoice_last_modified_at=datetime.fromisoformat('2024-04-23 18:33:36.968453')
        )

        invoice_from_db = InvoiceView.query.get(1)

        self.assertEqual(invoice.invoice_id, invoice_from_db.invoice_id)
        self.assertEqual(invoice.invoice_reservation_id, invoice_from_db.invoice_reservation_id)
        self.assertEqual(invoice.invoice_date, invoice_from_db.invoice_date)
        self.assertEqual(invoice.invoice_price_gross, invoice_from_db.invoice_price_gross)
        self.assertEqual(invoice.invoice_is_paid, invoice_from_db.invoice_is_paid)
        self.assertEqual(invoice.invoice_status_id, invoice_from_db.invoice_status_id)
        self.assertEqual(invoice.invoice_last_modified_by, invoice_from_db.invoice_last_modified_by)
        self.assertEqual(invoice.invoice_last_modified_at, invoice_from_db.invoice_last_modified_at)

        self.assertEqual(
            repr(invoice),
            f'<InvoiceView(invoice_id={invoice_from_db.invoice_id}, '
            f'invoice_reservation_id={invoice_from_db.invoice_reservation_id}, '
            f'invoice_date={invoice_from_db.invoice_date}, '
            f'invoice_price_gross={invoice_from_db.invoice_price_gross}, '
            f'invoice_is_paid={invoice_from_db.invoice_is_paid}, '
            f'invoice_status_id={invoice_from_db.invoice_status_id}, '
            f'invoice_last_modified_by={invoice_from_db.invoice_last_modified_by}, '
            f'invoice_last_modified_at={invoice_from_db.invoice_last_modified_at})>'
        )
