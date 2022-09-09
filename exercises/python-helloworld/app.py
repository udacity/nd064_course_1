from email.mime import application
import json
import mimetypes
from urllib import response
from flask import Flask
app = Flask(__name__)



@app.route('/status')
def status():
    response = app.response_class( 
            response=json.dumps({"result":"OK - healthy"}), #json.dumps() converts python object it a json string
            status=200, #this refers to the http requests has been succesfully served
            mimetype='application/json' #format of the response data 
    )

    return response
    

@app.route('/metrics')
def metrics():
    response = app.response_class( 
            response=json.dumps({"status":"success","code":0,"data":{"UserCount": 140, "UserCountActive": 23}}), #json.dumps() converts python object it a json string
            status=200, #this refers to the http requests has been succesfully served
            mimetype='application/json' #format of the response data 
    )

    return response

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
