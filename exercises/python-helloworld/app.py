
from flask import Flask,render_template,request
from flask import json

import logging

app = Flask(__name__)
app.debug=True
app.secret_key="secret key"

# @app.route("/status")
# def status_healthcheck():
#     result={"result":"OK- healthy"}
#     response = app.response_class(json.dumps(result),status=200,mimetype="application/json")
#     app.logger.info("Status request successful")
#     return response

# @app.route("/metrics")
# def metrics():
#     result={
#                 "status":"success",
#                 "code":0,
#                 "data":{
#                             "UserCount":149,
#                             "UserCountActive":20
#                         }
#             }
#     response = app.response_class(json.dumps(result),status=200,mimetype="application/json")
#     app.logger.info("Metrics request successful")
#     return response

# @app.route("/catalog")
# def catalog():
#     result={"url":"http://192.168.1.116:80/kmsdev/catalog/vehicles/index.php"}
#     return app.response_class(json.dumps(result),status=200,mimetype="application/json")

# @app.route("/", methods=['GET','POST'])
# def index():
    
#     app.logger.info("Index request successful")
#     return render_template('index.html')
# if __name__ == "__main__":

#     logging.basicConfig(filename="app.log",level=logging.DEBUG)

#     app.run(host='0.0.0.0')
