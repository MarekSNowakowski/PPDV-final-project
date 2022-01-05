from flask import Flask
import requests
import json

app = Flask(__name__)

@app.route('/')
def main():
    uri = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/2"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    #data = json.loads(Jresponse)

    return Jresponse

if __name__ == "__main__":
    app.run()