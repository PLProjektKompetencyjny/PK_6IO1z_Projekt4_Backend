import logger
from flask import Flask

logger.configure_logging()

app = Flask(__name__)


@app.route('/')
def hello_world():
    app.logger.info("Hello, World!")
    return 'Hello, World!'


@app.route('/error')
def error():
    app.logger.error("I'm an error")
    return "I'm an error"


@app.after_request
def after_request(response):
    app.logger.info(f"Request status: {response.status_code}")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
