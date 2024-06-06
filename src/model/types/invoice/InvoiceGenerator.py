from logging import getLogger

from sqlalchemy.exc import SQLAlchemyError

from src.model.views.invoice_view import InvoiceView
from src.model.views.reservation_view import ReservationView
from src.model.views.customer_view import CustomerView
from src.model.views.service_view import ServiceView
from src.env import INVOICE_TEMPLATE_PATH

logger = getLogger(__name__)

class InvoiceGenerator:
    def __init__(self, reservation_id, tax):

        self.tax = tax
        self.tax_decimal = ((100 + self.tax) / 100)
        self.__details = []
        try:
            self.__reservation = ReservationView.get_details_for_invoice_about_reservation(reservation_id, logger)
            self.__invoice_view_details = InvoiceView.get_invoice_details_for_single_reservation(reservation_id, logger)
            self.__customer_details =CustomerView.get_customer_details_by_id(reservation_id, logger)
            self.__service_details = ServiceView.get_services_by_reservation_id(reservation_id, logger)
            self.__reservation_details = ReservationView.get_details_for_invoice_about_reservation(reservation_id, logger)
        except SQLAlchemyError as e:
            raise e

        self.__invoice_date = self.__invoice_view_details.invoice_date.strftime('%m-%d-%Y')


        for room in self.__reservation_details:
            self.__details.append([room.room_id,
                                         f'Adults: {room.number_of_adults}, children: {room.number_of_children}',
                                   room.duration.days,
                                   room.gross_price_room,
                                   room.duration.days * room.gross_price_room]
                                  )

        for service in self.__service_details:
            self.__details.append(['',
                                   f'Service: {service.service_name}',
                                   int(service.service_quantity),
                                   service.service_price,
                                   service.service_price * service.service_quantity]
                                  )

        self.template_path = INVOICE_TEMPLATE_PATH

        self.__invoice_data = {'id': self.__invoice_view_details.invoice_id,
                                        'reservation_id': reservation_id,
                                        'invoice_date': self.__invoice_date,
                                        'name': f'{self.__customer_details.customer_name} {self.__customer_details.customer_surname}',
                                        'address': f'{self.__customer_details.customer_street} {self.__customer_details.customer_building_number}, '
                                                   f'{self.__customer_details.customer_postal_code} {self.__customer_details.customer_city}',
                                        'mail': self.__customer_details.customer_email,
                                        'phone': self.__customer_details.customer_phone,
                                        'tax': f'{tax}%',
                                        'nip': self.__customer_details.customer_nip_number if self.__customer_details.customer_nip_number is not None else '',
                                        'net_total': self.__invoice_view_details.invoice_price_gross,
                                        'invoice_list': self.__details,
                                        'total': self.__invoice_view_details.invoice_price_gross * self.tax_decimal
                                        }

    def get_invoice_data(self):
        return self.__invoice_data

    def get_invoice_id(self):
        return self.__invoice_view_details.invoice_id

    def get_invoice_date(self):
        return self.__invoice_date