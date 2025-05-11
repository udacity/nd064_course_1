from flask import Flask
from flask import json
import logging

app = Flask(__name__)

# Set up logging to a file
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

# Also capture Werkzeug logs (for request info)
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.addHandler(file_handler)

@app.route('/status')
def status():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Status request successfull')
    app.logger.debug('DEBUG message')
    return response

@app.route('/metrics')
def metrics():
    response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
            status=200,
            mimetype='application/json'
    )
    app.logger.info('Metrics request successfull')
    return response

@app.route("/")
def hello():
    app.logger.info('Main request successfull')

    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
