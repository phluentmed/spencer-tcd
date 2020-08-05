from Interfaces.DataExporter import DataExporter
from Utilities.EventScheduler import EventScheduler

import logging
import json
#import requests

class HTTPExporter(DataExporter):

	def __init__(self, host_address, requests):
		self._host_address = host_address
		self._event_scheduler = EventScheduler("http_thread")
		self._is_running = False
		self._requests = requests

	def start(self):
		#TODO: have some retry logic on connect
		if not self._is_running:
			self._is_running = True
			return self._event_scheduler.start()
		logging.warning("HTTPExporter is already running")
		return -1

	def stop(self):
		if self._is_running:
			self._is_running = False
			return_code = self._event_scheduler.stop()
			return return_code
		logging.warning("HTTPExporter has already been stopped")
		return -1

	def export(self, data, result_handler):
		if self._is_running:
			self._event_scheduler.enter(0,
										1,
										self._export_dispatched,
										(data, result_handler))
			return 0
		logging.info("HTTPExporter has not been started")
		return -1

	def _export_dispatched(self, data, result_handler):
		#TODO add negling
		if data:
			response = self._requests.put(self._host_address,
									data=json.dumps(data))
			if response.status_code != 200:
				logging.error("Error sending data to " + self._host_address +
						" with http error code: " + str(response.status_code))
