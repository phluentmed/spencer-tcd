import json
import requests
import threading

from Components.PacketDecoder import PacketDecoder
from Components.CSVExporter import CSVExporter
from Components.HttpExporter import HttpExporter

class Controller():

	### constructor. called from main script ###
	def __init__(self, serial_connection, usb_port, out_file='', web_out=''):
		self._serial_connection = serial_connection(usb_port)
		self._out_file = out_file
		self._web_out = web_out
		self._is_running = False

		self._data_handler_thread = \
		threading.Thread(target=data_handler(self.handler_callback, \
		self.exporter_lst))

		self.exporter_lst = []
		self._is_running_lock = threading.Lock()


	@property
	def handler_callback(callback_code):
		print('Function callback code: ' + callback_code)

	@property
	def is_running(self):
		return self._is_running

	def start(self):
		if not self.is_running:
			self._is_running = True
			return self._data_handler.start()
		return -1

	def stop(self):
		with self._is_running_lock:
			if self.is_running:
				self._is_running = False
				for exporter in exporter_lst:
					exporter.stop()
				rc = self._data_handler_thread.stop()
				if (rc != 0):
					return rc
				return rc


	def data_handler(self, handler_callback, exporter_lst):

		### establish connection ###
		print('Result of serial connect: %r' % self._serial_connection.connect())
		packet_decoder = PacketDecoder.getInstance()

		# make list of exporters
		if self._out_file != None:
			self.exporter_lst.append(CSVExporter(self._out_file))
		if self._web_out != None:
			self.exporter_lst.append(HttpExporter(self._web_out))


		while self._is_running:
			header, data = serial_connection.receive()
			(PS, PL, DID, VER, PN, CH, PT) = header
			if not data and not header:
				print('error in transmission')
			if (PT == 1):
				print("envelope packet\n")

			# numerics packet sent once a second
			elif (PT == 2):
				print('numerics packet')
				num_packet = packet_decoder.decode(header, data)
				print(num_packet)

				for exporter in exporter_lst:
					## export to each available destination
					exporter.export(num_packet, \
					handler_callback(callback_code))

			# messages packet
			elif (PT == 3):
				print("message packet")
				print(packet_decoder.decode(header, data))

			# error packet
			elif (PT == 4):
				print("error packet")
				print(packet_decoder.decode(header, data))
