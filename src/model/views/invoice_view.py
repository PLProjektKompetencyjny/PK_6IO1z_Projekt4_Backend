from src.utils.utils import db


class InvoiceView(db.Model):
    __tablename__ = 'invoice_view'

    invoice_id = db.Column('invoice_id', db.Integer, primary_key=True)
    invoice_reservation_id = db.Column('invoice_reservation_id', db.Integer)
    invoice_date = db.Column('invoice_date', db.DateTime)
    invoice_status_id = db.Column('invoice_status_id', db.Integer)
    invoice_last_modified_by = db.Column('invoice_last_modified_by', db.String)
    invoice_last_modified_at = db.Column('invoice_last_modified_at', db.DateTime)

    def __repr__(self):
        return (
            f'<InvoiceView(invoice_id={self.invoice_id}, '
            f'invoice_reservation_id={self.invoice_reservation_id}, '
            f'invoice_date={self.invoice_date}, '
            f'invoice_status_id={self.invoice_status_id}, '
            f'invoice_last_modified_by={self.invoice_last_modified_by}, '
            f'invoice_last_modified_at={self.invoice_last_modified_at})>'
        )
