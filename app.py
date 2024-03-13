import logger
from flask import Flask

logger.configure_logging()

app = Flask(__name__)


@app.route('/')
def hello_world():
    message = "Hello, World!"
    app.logger.info(f"{message}")
    return message


@app.route('/error')
def error():
    error_message = "I'm an error"
    app.logger.error(f"{error_message}")
    return error_message


@app.after_request
def after_request(response):
    app.logger.info(f"Request status: {response.status_code}")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
