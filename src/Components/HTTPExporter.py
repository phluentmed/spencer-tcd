from Interfaces.DataExporter import DataExporter
from Utilities.EventScheduler import EventScheduler

import json
import requests

class HTTPExporter(DataExporter):

	def __init__(self, host_address):
		self._host_address = host_address
		self._event_scheduler = EventScheduler("http_thread")
		self._is_running = False

	def start(self):
		#TODO: have some retry logic on connect
		if not self._is_running:
			self._is_running = True
			return self._event_scheduler.start()
		#TODO add some message of failure saying already running or failed
		return -1

	def stop(self):
		if self._is_running:
			self._is_running = False
			return_code = self._event_scheduler.stop()
			self._export_dispatched(None, True)
			return return_code
		return -1

	def export(self, data, result_handler):
		if self._is_running:
			self._event_scheduler.enter(0,
										1,
										self._export_dispatched,
										(data, result_handler))
		#TODO add helpful message for feedback
		return -1

	def _export_dispatched(self, data, result_handler):
		#TODO add negling
		if data:
			response = requests.put(self._host_address,
									data=json.dumps(data))
			if response.status_code != 200:
				print("Error sending data to " + self._host_address +
					  " with error code" + response.status_code)
				raise Exception('Failed to export')
			return response.status_code
