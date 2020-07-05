import json
import requests
from multiprocessing import Process

from Components.SerialConnection import SerialConnection
from Components.PacketDecoder import PacketDecoder
from Components.CSVExporter import CSVExporter
from Components.HttpExporter import HttpExporter

class Controller():

	### constructor. called from main script ###
	def __init__(self, baud, out_file='', web_out=''):
		self._baud = baud
		self._out_file = out_file
		self._web_out = web_out
		self._is_running = False

	@property
	def is_running(self):
		return self._is_running
	
	def start(self):
		if not self.is_running:
			self._is_running = True
			return self.start() ## fix
		return -1

	def stop(self):
		if self.is_running:
			self._is_running = False
			rc = self.stop() ## fix
			if (rc != 0):
				return rc
			self.stop() ## fix
			return rc
	
	def data_handler(self, handler_callback):

		### establish connection ###
		serial_connection = SerialConnection(self.port)
		print('Result of serial connect: %r' % serial_connection.connect())
		packet_decoder = PacketDecoder.getInstance()

		# make list of exporters
		exporter_lst = []
			if self._out_file != None:
				exporter_lst.append(CSVExporter)
			if self._web_out != None:
				exporter_lst.append(HttpExporter)


		while True:
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
					exporter.export() ## export to each available destination

			# messages packet
			elif (PT == 3):
				print("message packet")
				print(packet_decoder.decode(header, data))
			
			# error packet
			elif (PT == 4):
				print("error packet")
				print(packet_decoder.decode(header, data))

			

	def tcd_network_post(payload, dest_ip): ## idk if we still need this fn here?
		print("called tcd_network_post")
		payload = {'TCDMonitor': payload}
		print(payload)
		r = requests.put(dest_ip, data=json.dumps(payload))
		print(r.text)

	### I know we're supposed to do some error stuff here. but i don't get why/how
	# my understanding a callback function is that it just runs at the 
	# end of the function it was passed into
	###
	def handler_callback():
		print('data handler completed')


	### run data_handler in its own process ### 
	data_listen = Process(target=data_handler)

