import os
import stripe

from logging import getLogger
from src.model.views.invoice_view import InvoiceView
from src.model.views.reservation_view import ReservationView
from sqlalchemy.exc import SQLAlchemyError
from src.utils.utils import sqlalchemy_error_to_dict
from src.env import STRIPE_KEY

stripe.api_key = STRIPE_KEY

logger = getLogger(__name__)


def generate_payment_link_and_update_invoice(reservation_id: int):
    amount = 0  # in pennies
    amount_in_usd = InvoiceView.get_gross_price_for_reservation(reservation_id, logger)
    amount = amount_in_usd*100
    amount_with_tax = amount*1.08  # tax is 8%, amount_with_tax must be in pennies

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Hotel room',
                    },
                    'unit_amount': int(amount_with_tax),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:80/payment/success',
            cancel_url='http://localhost:80/payment/fail'
        )
        InvoiceView.set_invoice_payment_id(reservation_id, session.id, logger)
        return session.url
    except stripe.error.StripeError as e:
        print("Error occurred:", e)


def get_payment_ids_to_check():
    reservations = ReservationView.get_non_paid_reservations(logger)
    payment_ids_to_check = []

    for reservation in reservations:
        try:
            payment_ids_to_check.append(InvoiceView.get_payment_id(reservation[0], logger))
        except SQLAlchemyError as e:
            json_data_error = sqlalchemy_error_to_dict(e)
            logger.error(json_data_error)
            raise e
    return payment_ids_to_check


def get_payment_status(payment_id):
    try:
        session = stripe.checkout.Session.retrieve(payment_id)
        return session['payment_status']
    except stripe.error.StripeError as e:
        return None