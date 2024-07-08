import os
import sys

from logging import getLogger
from apscheduler.schedulers.background import BackgroundScheduler
from src.model.views.invoice_view import InvoiceView
from src.model.views.reservation_view import ReservationView
from src.service.payments.payments import get_payment_status

logger = getLogger(__name__)


def setup_scheduler_for_payments(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_for_payments_statuses, 'interval', seconds=60, args=[app])
    scheduler.start()


def check_for_payments_statuses(app):
    with app.app_context():
        print('Checking for payments statuses', file=sys.stderr)
        non_paid_reservations = ReservationView.get_non_paid_reservations(logger)
        for reservation in non_paid_reservations:
            reservation_id = reservation[0]
            payment_id = InvoiceView.get_payment_id(reservation_id, logger)
            if payment_id != 0 and payment_id is not None:
                payment_status = get_payment_status(payment_id)
                if payment_status is not None:
                    print(f"Payment status {payment_status} for payment id {payment_id}", file=sys.stderr)
                    if payment_status == 'paid':
                        ReservationView.set_reservation_as_paid(reservation_id)
                else:
                    print(f"Couldn't get status for payment id {payment_id}", file=sys.stderr)
