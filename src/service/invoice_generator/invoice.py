import docxtpl
import subprocess
import sys
import re
from os import path, remove


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

        self.invoice_view_details = db.session.query(
                                        InvoiceView
                                    ).filter(
            InvoiceView.invoice_reservation_id == reservation_id
                                    ).first()

        self.invoice_date = self.invoice_view_details.invoice_date.strftime('%m-%d-%Y')
        self.invoice_id = self.invoice_view_details.invoice_id

        self.customer_details = db.session.query(
                                    CustomerView
                                ).join(
                                    ReservationView,
                                    onclause=ReservationView.reservation_customer_id == CustomerView.customer_id
                                ).filter(
                                    ReservationView.reservation_id == self.invoice_view_details.invoice_reservation_id
                                ).first()

        self.reservation_details = db.session.query(
                ReservationView.reservation_id,
                ReservationView.reservation_room_id,
                ReservationView.reservation_number_of_adults,
                ReservationView.reservation_number_of_children,
                ReservationView.reservation_end_date - ReservationView.reservation_start_date,
                (
                        RoomView.room_gross_price +
                        (RoomView.room_gross_price_adult * ReservationView.reservation_number_of_adults)+
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

        self.reservation_id = self.reservation_details[0][0]


        self.tax = tax
        self.tax_decimal = ((100-self.tax)/100)
        self.rooms_details = []
        self.gross_prices = []
        self.net_prices =[]

        for room in self.reservation_details:
            self.gross_prices.append((room[4].days * room[5]))

            self.net_prices.append(round(self.gross_prices[-1] * self.tax_decimal, 2))

            self.rooms_details.append([room[1],
                                       f'Adults: {room[2]}, children: {room[3]}',
                                       room[4].days,
                                       round(room[5]*self.tax_decimal, 2),
                                       self.net_prices[-1]]
                                      )

        self.template_path = "src/templates/INVOICE/Invoice_template.docx"

        self.data = {'id': self.invoice_id,
                     'reservation_id': self.reservation_id,
                     'invoice_date': self.invoice_date,
                     'name': f'{self.customer_details.customer_name} {self.customer_details.customer_surname}' ,
                     'address': f'{self.customer_details.customer_street} {self.customer_details.customer_building_number}, '
                                f'{self.customer_details.customer_postal_code} {self.customer_details.customer_city}',
                     'mail': self.customer_details.customer_email,
                     'phone': self.customer_details.customer_phone,
                     'tax': f'{tax}%',
                     'nip':self.customer_details.customer_nip_number if self.customer_details.customer_nip_number is not None else '',
                     'net_total': sum(self.net_prices),
                     'invoice_list': self.rooms_details,
                     'total': sum(self.gross_prices)
                     }
    def generate(self):
        invoice_file_obj = docxtpl.DocxTemplate(self.template_path)
        invoice_file_obj.render(self.data)
        docx_file_name = f'{self.invoice_id}_{self.invoice_date}_invoice.docx'
        temp_path = 'temp/'
        docx_file_name = path.join(temp_path, docx_file_name)
        invoice_file_obj.save(docx_file_name)

        pdf_path = convertDocxToPdf(docx_file_name, temp_path)
        remove(docx_file_name)

        return pdf_path

