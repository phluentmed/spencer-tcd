from Interfaces.DataExporter import DataExporter
from Utilities.EventScheduler import EventScheduler

import json


class HTTPExporter(DataExporter):

    def __init__(self, host_address, requests):
        self._host_address = host_address
        self._event_scheduler = EventScheduler("http_thread")
        self._is_running = False
        self._requests = requests

    def start(self):
        # TODO: have some retry logic on connect
        if not self._is_running:
            rc = self._event_scheduler.start()
            if rc == 0:
                self._is_running = True
            return rc
        return -1

    def stop(self, result_handler=None):
        if self._is_running:
            rc = self._event_scheduler.stop()
            if rc == 0:
                self._is_running = False
            return rc
        return -1

    def export(self, data, result_handler):
        if self._is_running:
            self._event_scheduler.enter(0,
                                        1,
                                        self._export_dispatched,
                                        (data, result_handler))
            return 0
        return -1

    def _export_dispatched(self, data, result_handler):
        # TODO: add naggling
        if data:
            response = self._requests.put(self._host_address,
                                          data=json.dumps(data))
            if response.status_code == 200:
                result_handler(20, 'Record sent via http to ' +
                               self._host_address)
            if response.status_code != 200:
                result_handler(40, "Error sending data to " +
                               self._host_address + " with http error code: " +
                               str(response.status_code))
