import stripe
import sys

from logging import getLogger
from src.model.views.invoice_view import InvoiceView
from src.model.views.reservation_view import ReservationView
from sqlalchemy.exc import SQLAlchemyError

from src.utils.utils import sqlalchemy_error_to_dict

# stripe.api_key = "sk_test_51PYAfPRrnWZoSf4Vf5sEUCEys1olebpof755PM5QiOfAzDuR75HwRfm3Bc6m0NAiORgYTepykvsQHsdTr4kWYtXV00vi0jFSXp"
#
# amount = 1000 # 100 equals to 1 zł 00 groszy
#
# try:
#     session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[{
#             'price_data': {
#                 'currency': 'pln',
#                 'product_data': {
#                     'name': 'Hotel room',
#                 },
#                 'unit_amount': amount,
#             },
#             'quantity': 1,
#         }],
#         mode='payment',
#         success_url='http://localhost:80/payment/success',
#         cancel_url=' http://localhost:80/payment/fail',
#     )
#     print("Checkout Session created successfully:", session.url)
# except stripe.error.StripeError as e:
#     print("Error occurred:", e)

logger = getLogger(__name__)


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


