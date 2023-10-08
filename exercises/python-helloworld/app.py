from flask import Flask
import json
import logging

app = Flask(__name__)

@app.route("/status")
def healthcheck():
    response = app.response_class(
        response=json.dumps({"result": "OK - Healthy"}),
        status=200,
        mimetype="application/json"
    )
    ## log line
    app.logger.info('Status request successfull')
    return response

@app.route("/metrics")
def metrics():
    response = app.response_class(
        response=json.dumps({
            "status": "success",
            "code": 0,
            "data": {
                "userCount": 140,
                "userCountActive": 23
            }
        }),
        status=200,
        mimetype="application/json"
    )
    ## log line
    app.logger.info('Metrics request successfull')
    return response


@app.route("/")
def hello():
    # Logging a custom message
    app.logger.info("Main request successfull")
    return "Hello World!"

if __name__ == "__main__":
    # Stream logs to a file, and set the default log level to DEBUG
    logging.basicConfig(filename='app.log',level=logging.DEBUG)
    app.run(host='0.0.0.0')
