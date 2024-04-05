import docxtpl

from src.model.views.invoice_view import InvoiceView
from src.model.views.reservation_view import ReservationView
from src.model.views.customer_view import CustomerView

class InvoiceGenerator:
    def __init__(self, invoice_id):
        self.invoice_details = InvoiceView.query.filter(invoice_id=invoice_id).one()

        self.template_path = "../../templates/INVOICE/Invoice_template.docx"
        self.customers_details = CustomerView.query.join(
                                                        ReservationView, customer_id = ReservationView.reservation_customer_id).filter(
                                                        ReservationView.reservation_id == self.invoice_details.reservation_id
                                                        ).one()

        invoice_list = [
                        ['201', 'Room booking details: 1 child, 2 adults', 200, 200],
                        ['202', 'Room booking details: 2 adults', 100, 100]
                        ]

        net_total = 0
        for item in invoice_list: net_total += item[3]
        tax = 8
        self.data = {'id': invoice_id,
                     'invoice_date': self.invoice_details.invoice_date,
                     'name': f'{self.customers_details.customer_name} {self.customers_details.customer_surname}' ,
                     'address': f'{self.customers_details.customer_street} {self.customers_details.customer_building_number}, {self.customers_details.customer_street} {self.customers_details.customer_postal_code}',
                     'mail': self.customers_details.customer_email,
                     'phone': self.customers_details.customer_phone.customer_phone,
                     'tax': f'{tax}%',
                     'nip':self.customers_details.customer_nip_number,
                     'net_total': net_total,
                     'invoice_list': invoice_list,
                     'total': ((100+8)/100) * net_total
                     }



        self.invoice_file_obj = docxtpl.DocxTemplate(self.template_path)
        self.invoice_file_obj.render(self.data)
        self.invoice_file_obj.save('test.docx')


