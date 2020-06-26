import csv
from Interfaces.DataExporter import DataExporter
from Utilities.EventScheduler import EventScheduler

class CSVExporter(DataExporter):


    def __init__(self, filepath, max_buffer_size=10):
        self._filepath        = filepath
        self._event_scheduler = EventScheduler()
        self._max_buffer_size = max_buffer_size
        self._data_buffer     = []


    """
    Starts streaming data to the csv file. Returns 0 on success and a negative
    error code on failure.
    """
    def start(self):
        return self._event_scheduler.start()

    """
    Stops data export, and safely closes off destination.
    """
    def stop(self):
        rc, message = self._event_scheduler.stop()
        if (rc != 0):
            return rc, message
        self._export_dispatched(None, None, True)
        return rc

    """
    Receives data to be exported
    @param
    data: decoded data format 
    @param
    result_handler: called after the data export operation is completed.
    """
    def export(self, data, result_handler):
        self._event_scheduler.enter(0,
                                    1,
                                    self._export_dispatched,
                                    (data, result_handler))

    # Executed from the Event Scheduler thread
    def _export_dispatched(self, data, result_handler, flush_buffer=False):
        if flush_buffer and len(self._data_buffer):
            self._write_to_csv()
            # TODO: Invoke success handler once we know what it looks like
            return
        self._data_buffer.append(data)
        if len(self._data_buffer) < self._max_buffer_size:
            self._write_to_csv()
            # TODO: Invoke success handler once we know what it looks like
            return


    # Executed from the Event Scheduler thread
    def _write_to_csv(self):
        with open(self._filepath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=list(
                                                 self._data_buffer[0].keys()))
            if csvfile.tell() == 0:
                writer.writeheader()
            for data in self._data_buffer:
                writer.writerow(data)
            self._data_buffer.clear()
        # TODO: Try this write again in case it fails.