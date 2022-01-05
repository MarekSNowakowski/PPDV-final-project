import requests


def get_new_data(patient_id):
    uri = f"http://tesla.iem.pw.edu.pl:9080/v2/monitor/{patient_id}"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    jResponse = uResponse.json()

    return {
        "timestamp": jResponse["trace"]["id"],
        "values": [x["value"] for x in jResponse["trace"]["sensors"]],
        "anomalies": [x["anomaly"] for x in jResponse["trace"]["sensors"]]
    }
