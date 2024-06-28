from os import getenv

DB_ADDRESS = getenv('DB_Address', 'localhost')
DB_PORT = getenv('DB_Port', '5432')
DB_NAME = getenv('DB_Name', 'TravelNest')
DB_USERNAME = getenv('DB_Username', 'tn_api_write')
DB_PASSWORD = getenv('DB_Password', 'cba')

JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', 'tn_jwt_secret')

SECRET_KEY = getenv('SECRET_KEY', 'my_precious_secret_key')

INVOICE_DEST_PATH = getenv('INVOICE_DEST_PATH', default='/tmp')
INVOICE_TEMPLATE_PATH = getenv('INVOICE_TEMPLATE_PATH', default='src/templates/INVOICE/Invoice_template.docx')