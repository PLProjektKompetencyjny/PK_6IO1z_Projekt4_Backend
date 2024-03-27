from datetime import datetime

from src.model.views.invoice_view import InvoiceView
from src.utils.utils import db
from test import BaseTestCase


class TestInvoiceView(BaseTestCase):
    def test_invoice_view_repr(self):
        invoice = InvoiceView(
            invoice_id=1,
            invoice_reservation_id=1,
            invoice_date=datetime.now(),
            invoice_status_id=1,
            invoice_last_modified_by='John Doe',
            invoice_last_modified_at=datetime.now()
        )
        db.session.add(invoice)
        db.session.commit()

        invoice_from_db = InvoiceView.query.get(1)

        self.assertEqual(invoice.invoice_id, invoice_from_db.invoice_id)
        self.assertEqual(invoice.invoice_reservation_id, invoice_from_db.invoice_reservation_id)
        self.assertEqual(invoice.invoice_date, invoice_from_db.invoice_date)
        self.assertEqual(invoice.invoice_status_id, invoice_from_db.invoice_status_id)
        self.assertEqual(invoice.invoice_last_modified_by, invoice_from_db.invoice_last_modified_by)
        self.assertEqual(invoice.invoice_last_modified_at, invoice_from_db.invoice_last_modified_at)

        self.assertEqual(
            repr(invoice),
            f'<InvoiceView(invoice_id={invoice_from_db.invoice_id}, '
            f'invoice_reservation_id={invoice_from_db.invoice_reservation_id}, '
            f'invoice_date={invoice_from_db.invoice_date}, '
            f'invoice_status_id={invoice_from_db.invoice_status_id}, '
            f'invoice_last_modified_by={invoice_from_db.invoice_last_modified_by}, '
            f'invoice_last_modified_at={invoice_from_db.invoice_last_modified_at})>'
        )
