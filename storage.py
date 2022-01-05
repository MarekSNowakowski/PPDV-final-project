import time

global _storage


def init_storage():
    global _storage
    _storage = {}
    return _storage


def get_storage():
    global _storage
    return _storage


def add_measurements(patient_id, data):
    storage = get_storage()
    if patient_id not in storage:
        patient_data = {
            "timestamps": [],
            "values": [],
            "anomalies": [],
            "_expire_ts": []
        }
        storage[patient_id] = patient_data
    else:
        patient_data = storage[patient_id]

    patient_data["timestamps"].append(data["timestamp"])
    patient_data["values"].append(data["values"])
    patient_data["anomalies"].append(data["anomalies"])
    patient_data["_expire_ts"].append(time.time())


def expire_data(s):
    storage = get_storage()
    for patient_id, patient_data in storage.items():
        ts = time.time()
        while len(patient_data["_expire_ts"]) > 0 and patient_data["_expire_ts"][0] < (ts - s):
            patient_data["timestamps"].pop(0)
            patient_data["values"].pop(0)
            patient_data["anomalies"].pop(0)
            patient_data["_expire_ts"].pop(0)
