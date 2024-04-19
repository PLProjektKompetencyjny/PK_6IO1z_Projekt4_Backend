import datetime

import docxtpl
import subprocess
import sys
import re
from os import path, remove, getenv

from src.utils.utils import db
from src.model.views.invoice_view import InvoiceView
from src.model.views.reservation_view import ReservationView
from src.model.views.customer_view import CustomerView
from src.model.views.room_view import RoomView


def convertDocxToPdf(docx_file_path: str, destination_path: str, timeout=None):
    try:
        args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', destination_path, docx_file_path]

        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        filename = re.search('-> (.*?) using filter', process.stdout.decode())
    except FileNotFoundError:
        raise FileNotFoundError('')
    else:
        return filename.group(1)


class InvoiceGenerator:
    def __init__(self, reservation_id, tax):
        self.__invoice_view_details = db.session.query(
            InvoiceView
        ).filter(
            InvoiceView.invoice_reservation_id == reservation_id
        ).first()

        self.__customer_details = db.session.query(
            CustomerView
        ).join(
            ReservationView,
            onclause=ReservationView.reservation_customer_id == CustomerView.customer_id
        ).filter(
            ReservationView.reservation_id == self.__invoice_view_details.invoice_reservation_id
        ).first()

        self.__reservation_details = db.session.query(
            ReservationView.reservation_id,
            ReservationView.reservation_room_id,
            ReservationView.reservation_number_of_adults,
            ReservationView.reservation_number_of_children,
            ReservationView.reservation_end_date - ReservationView.reservation_start_date,
            (
                    RoomView.room_gross_price +
                    (RoomView.room_gross_price_adult * ReservationView.reservation_number_of_adults) +
                    (RoomView.room_gross_price_child * ReservationView.reservation_number_of_children)
            )
        ).join(
            InvoiceView,
            onclause=InvoiceView.invoice_reservation_id == ReservationView.reservation_id
        ).join(
            RoomView,
            onclause=RoomView.room_id == ReservationView.reservation_room_id
        ).filter(
            InvoiceView.invoice_id == reservation_id
        ).all()

        self.invoice_date = self.__invoice_view_details.invoice_date.strftime('%m-%d-%Y')
        self.invoice_id = self.__invoice_view_details.invoice_id
        self.reservation_id = self.__invoice_view_details.invoice_reservation_id

        self.tax = tax
        self.tax_decimal = ((100 - self.tax) / 100)
        self.__rooms_details = []
        self.__gross_prices = []
        self.__net_prices = []

        for room in self.__reservation_details:
            self.__gross_prices.append((room[4].days * room[5]))

            self.__net_prices.append(round(self.__gross_prices[-1] * self.tax_decimal, 2))

            self.__rooms_details.append([room[1],
                                         f'Adults: {room[2]}, children: {room[3]}',
                                         room[4].days,
                                         round(room[5] * self.tax_decimal, 2),
                                         self.__net_prices[-1]]
                                        )

        self.template_path = getenv('INVOICE_TEMPLATE_PATH', default='src/templates/INVOICE/Invoice_template.docx')

        self.__invoice_template_data = {'id': self.invoice_id,
                                        'reservation_id': self.reservation_id,
                                        'invoice_date': self.invoice_date,
                                        'name': f'{self.__customer_details.customer_name} {self.__customer_details.customer_surname}',
                                        'address': f'{self.__customer_details.customer_street} {self.__customer_details.customer_building_number}, '
                                                   f'{self.__customer_details.customer_postal_code} {self.__customer_details.customer_city}',
                                        'mail': self.__customer_details.customer_email,
                                        'phone': self.__customer_details.customer_phone,
                                        'tax': f'{tax}%',
                                        'nip': self.__customer_details.customer_nip_number if self.__customer_details.customer_nip_number is not None else '',
                                        'net_total': sum(self.__net_prices),
                                        'invoice_list': self.__rooms_details,
                                        'total': sum(self.__gross_prices)
                                        }

    def generate(self):
        invoice_file_obj = docxtpl.DocxTemplate(self.template_path)
        invoice_file_obj.render(self.__invoice_template_data)
        now = datetime.datetime.now()
        docx_file = f"{self.invoice_id}_{self.invoice_date}_invoice_{now.hour}_{now.minute}_{now.second}.docx"

        docx_file = path.join('/tmp', docx_file)
        invoice_file_obj.save(docx_file)

        pdf_dest_path = getenv('INVOICE_PATH', default='/tmp')
        pdf_dest_path = convertDocxToPdf(docx_file, pdf_dest_path)

        try:
            remove(docx_file)
        except FileNotFoundError:
            pass

        return pdf_dest_path
