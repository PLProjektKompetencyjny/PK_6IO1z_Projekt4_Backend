import datetime
from os import path, remove

import docxtpl
import subprocess
import re

from src.model.types.invoice import InvoiceGenerator
from src.env import INVOICE_DEST_PATH

def convertDocxToPdf(docx_file_path: str, destination_path: str, timeout=None):
    try:
        args = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', destination_path, docx_file_path]

        process = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        filename = re.search('-> (.*?) using filter', process.stdout.decode())
    except FileNotFoundError:
        raise FileNotFoundError('Not found file in specified directory')
    else:
        return filename.group(1)


def generate(generatorObject: InvoiceGenerator):
    invoice_file_obj = docxtpl.DocxTemplate(generatorObject.template_path)
    invoice_file_obj.render(generatorObject.get_invoice_data())
    now = datetime.datetime.now()
    docx_file = f"{generatorObject.get_invoice_id()}_{generatorObject.get_invoice_date()}_invoice_{now.hour}_{now.minute}_{now.second}.docx"
    docx_file = path.join('/tmp', docx_file)
    invoice_file_obj.save(docx_file)

    pdf_dest_path = INVOICE_DEST_PATH
    pdf_dest_path = convertDocxToPdf(docx_file, pdf_dest_path)
    try:
        remove(docx_file)
    except FileNotFoundError as e:
        raise e
      
    return pdf_dest_path