from os import getenv

DB_ADDRESS = getenv('DB_Address', 'localhost')
DB_PORT = getenv('DB_Port', '5432')
DB_NAME = getenv('DB_Name', 'TravelNest')
DB_USERNAME = getenv('DB_Username', 'tn_api_write')
DB_PASSWORD = getenv('DB_Password', 'cba')

JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', 'tn_jwt_secret')

INVOICE_DEST_PATH = getenv('INVOICE_DEST_PATH', default='/tmp')
INVOICE_TEMPLATE_PATH = getenv('INVOICE_TEMPLATE_PATH', default='src/model/templates/INVOICE/invoice_template.docx')

STRIPE_KEY = getenv("STRIPE_KEY", "sk_test_51PYAfPRrnWZoSf4Vf5sEUCEys1olebpof755PM5QiOfAzDuR75HwRfm3Bc6m0NAiORgYTepykvsQHsdTr4kWYtXV00vi0jFSXp")
SECRET_KEY = getenv('SECRET_KEY', 'my_precious_secret_key')

LOGO_HTTPS_PATH = getenv('LOGO_HTTPS_PATH', default='https://lh3.googleusercontent.com/d/1fBRxFZ_CbRr99CYcK89wAqAmr4PVbdKE')
EMAIL_ADDRESS = getenv('EMAIL_ADDRESS', default='travelnest2407@gmail.com')
EMAIL_PASS = getenv('EMAIL_PASS', default='ssym dqry bsdz nlzd')
