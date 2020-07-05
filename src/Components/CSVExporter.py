import csv
from Interfaces.DataExporter import DataExporter
from Utilities.EventScheduler import EventScheduler


class CSVExporter(DataExporter):

    def __init__(self, filepath, max_buffer_size=10):
        self._filepath = filepath
        self._event_scheduler = EventScheduler("csv_thread")
        self._max_buffer_size = max_buffer_size
        self._data_buffer = []
        self._is_running = False

    @property
    def is_running(self):
        """Starts streaming data to the csv file. Returns 0 on success and a
            negative
            error code on failure.
        """
        return self._is_running

    """
    Starts streaming data to the csv file. Returns 0 on success and a negative
    error code on failure.
    """
    def start(self):
        if not self.is_running:
            self._is_running = True
            return self._event_scheduler.start()
        return -1

    """
    Stops data export, and safely closes off destination.
    """
    def stop(self):
        if self.is_running:
            self._is_running = False
            rc = self._event_scheduler.stop()
            if (rc != 0):
                return rc
            self._export_dispatched(None, None, True)
            return rc
        return -1

    """
    Receives data to be exported
    @param
    data: decoded data format 
    @param
    result_handler: called after the data export operation is completed.
    """
    def export(self, data, result_handler):
        if self.is_running:
            self._event_scheduler.enter(0,
                                        1,
                                        self._export_dispatched,
                                        (data, result_handler))
            return 0
        return -1

    # Executed from the Event Scheduler thread
    def _export_dispatched(self, data, result_handler, flush_buffer=False):
        if data:
            self._data_buffer.append(data)
        if self._data_buffer and \
           len(self._data_buffer) >= self._max_buffer_size:
            self._write_to_csv()
            # TODO: Invoke success handler once we know what it looks like
            return
        if flush_buffer and self._data_buffer:
            self._write_to_csv()
            # TODO: Invoke success handler once we know what it looks like
            return

    # Executed from the Event Scheduler thread
    def _write_to_csv(self):
        with open(self._filepath, 'a') as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=list(
                                                 self._data_buffer[0].keys()))
            if csvfile.tell() == 0:
                writer.writeheader()
            for data in self._data_buffer:
                writer.writerow(data)
            self._data_buffer.clear()
        # TODO: Try this write again in case it fails.