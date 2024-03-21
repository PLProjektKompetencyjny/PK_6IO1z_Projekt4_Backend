from flask import Flask, redirect, url_for, session
from oauth2client.service_account import ServiceAccountCredentials
import json

app = Flask(__name__)
app.secret_key = 'super secret key'


SERVICE_ACCOUNT_FILE = 'google_credentials.json'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Funkcja do uzyskania uwierzytelnienia za pomocą pliku klucza usługi
def get_credentials():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        SERVICE_ACCOUNT_FILE, SCOPES)
    return credentials

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    credentials = get_credentials()
    session['credentials'] = credentials.to_json()
    return redirect(url_for('authorized'))

@app.route('/logout')
def logout():
    session.pop('credentials', None)
    return redirect(url_for('index'))

@app.route('/authorized')
def authorized():
    credentials_json = session.get('credentials')
    if credentials_json:
        credentials = ServiceAccountCredentials.from_json(json.loads(credentials_json))
        # Tutaj możesz użyć credentials do wysłania wiadomości e-mail
        return 'Logged in!'
    else:
        return 'Access denied!'


@app.route('/send_mail/<string:mail>?<string:subject>', methods = ['POST'])
def send_mail(mail:str, subject:str):
    print(1)


if __name__ == '__main__':
    app.run(debug=True)
