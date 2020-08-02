import threading

from Components.PacketDecoder import PacketDecoder
from Components.CSVExporter import CSVExporter
# from Components.HttpExporter import HttpExporter

class Controller():

	### constructor. called from main script ###
	def __init__(self, serial_connection, usb_port, out_file='', web_out=''):
		self._serial_connection = serial_connection(usb_port)
		self._out_file = out_file
		self._web_out = web_out
		self._is_running = False
		self._exporter_lst = []
		self._data_handler_thread = \
		threading.Thread(target=self._data_handler, \
		args=[self.handler_callback])

	def handler_callback(self, callback_code):
		print('Function callback code: ' + str(callback_code))

	@property
	def is_running(self):
		return self._is_running

	def start(self):
		if not self.is_running:
			self._is_running = True
			self._data_handler_thread.start()
		return 0

	def stop(self):
		for exporter in self._exporter_lst:
			exporter.stop()
		self._is_running = False
		self._serial_connection.cancel_read()
		self._data_handler_thread.join()
		return 0


	def _data_handler(self, handler_callback):

		### establish connection ###
		print('Result of serial connect: %r' % self._serial_connection.connect())
		packet_decoder = PacketDecoder.getInstance()

		# make list of exporters
		if self._out_file:
			self._exporter_lst.append(CSVExporter(self._out_file))
		if self._web_out:
			self._exporter_lst.append(HttpExporter(self._web_out))

		for exporter in self._exporter_lst:
			exporter.start()

		while self._is_running:
			header, data = self._serial_connection.receive()

			(PS, PL, DID, VER, PN, CH, PT) = header
			if not data and not header:
				print('error in transmission')
			if (PT == 1):
				print("envelope packet\n")

			# numerics packet sent once a second
			elif (PT == 2):
				# print('numerics packet')
				num_packet = packet_decoder.decode(header, data)
				# print(num_packet)

				for exporter in self._exporter_lst:
					## export to each available destination
					exporter.export(num_packet, \
					handler_callback)

			# messages packet
			elif (PT == 3):
				print("message packet")
				print(packet_decoder.decode(header, data))

			# error packet
			elif (PT == 4):
				print("error packet")
				print(packet_decoder.decode(header, data))
