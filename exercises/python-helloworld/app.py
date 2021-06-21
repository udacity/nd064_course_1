import logging

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    app.logger.info('Hello request successfull')
    return "Hello World!"


@app.route("/status")
def status():
    app.logger.info('Status request successfull')
    return {"result": "OK - healthy"}

@app.route("/metrics")
def metrics():
    app.logger.info('Metrics request successfull')
    return {"UserCount": 140, "UserCountActive": 23}

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    app.run(host='0.0.0.0')
