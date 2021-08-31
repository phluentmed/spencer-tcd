import logging
import requests
import threading
import datetime

from Components.PacketDecoder import PacketDecoder
from Components.CSVExporter import CSVExporter
from Components.HTTPExporter import HTTPExporter

logger = logging.getLogger()

class Controller():

    def __init__(self, serial_connection, usb_port, out_file='', web_out=''):
        self._serial_connection = serial_connection(usb_port)
        self._out_file = out_file
        self._web_out = web_out
        self._is_running = False
        self._exporter_lst = []
        self._data_handler_thread = \
            threading.Thread(target=self._data_handler)

    @property
    def is_running(self):
        return self._is_running

    def _handler_callback(self, level, message):
        logger.log(level, message)

    def start(self):
        if not self.is_running:
            self._is_running = True
            self._data_handler_thread.start()
            logger.info('Starting controller')
        return 0

    def stop(self):
        logger.info('Stopping controller')
        for exporter in self._exporter_lst:
            exporter.stop(self._handler_callback)
        self._is_running = False
        self._serial_connection.cancel_read()
        self._data_handler_thread.join()
        logger.info('Controller stopped.')
        return 0

    def _data_handler(self):
        # establish connection
        logger.info('TCD Connecting...')
        result = self._serial_connection.connect()
        if result:
            logger.info('TCD Connected')
        else:
            logger.error('TCD couldn\'t connect')
            # TODO: Handle when the TCD can't connect gracefully
        packet_decoder = PacketDecoder.get_instance()

        # make list of exporters
        if self._out_file:
            self._exporter_lst.append(CSVExporter(self._out_file))
        if self._web_out:
            self._exporter_lst.append(HTTPExporter(self._web_out, requests))

        for exporter in self._exporter_lst:
            exporter.start()

        while self._is_running:
            header, data = self._serial_connection.receive()

            (PS, PL, DID, VER, PN, CH, PT) = header
            if not data and not header:
                logger.error('TCD packet could not be correctly parsed')

            # envelope packet
            if PT == 1:
                pass

            # numerics packet sent once a second
            elif PT == 2:
                num_packet = packet_decoder.decode(header, data)
                for exporter in self._exporter_lst:
                    # export to each available exporter
                    exporter.export(num_packet, self._handler_callback)

            # messages packet
            elif PT == 3:
                print("message packet")
                logger.info('%s', packet_decoder.decode(header, data))

            # error packet
            elif PT == 4:
                logger.error('%s', packet_decoder.decode(header, data))
