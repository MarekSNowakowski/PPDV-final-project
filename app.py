from api_client import get_new_data
from storage import *
import threading
import time
from dash_app import app, create_layout

collector_running = True


class DataCollectorThread(threading.Thread):
    def run(self):
        while collector_running:
            add_measurements(2, get_new_data("2"))
            expire_data(20)
            print(get_storage())
            time.sleep(1)


if __name__ == "__main__":
    # Initialization
    init_storage()
    create_layout()
    # Start the collector
    collector = DataCollectorThread()
    collector.start()
    # Start dash app
    app.run_server(debug=True)

