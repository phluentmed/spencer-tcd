from collections import deque
from Components.SerialConnection import SerialConnection
import struct
import threading


class MockSerialConnection(SerialConnection):
    _header_unpacker = struct.Struct('H 6B')
    _HEADER_SIZE = 8
    _checksum_unpacker = struct.Struct('H')
    is_demo = False
    _numeric_packet = b'\xc3\xa50\xd1\x03\xe5\x01\x02\xd7\xfa\xcf4i\x01\x00' \
                      b'\x00\x01\x00       ' \
                      b'\x00\x002\n\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                      b'\x00\x00\x00\x00\x00\x00\x00\xb5\x07'

    def __init__(self,
                 usb_port):
        self._usb_port = usb_port
        self._is_open = False
        self._fake_data = deque()
        self._fake_data_lock = threading.RLock()
        self._cancel_read = False
        self._timer = None

    def is_connected(self):
        return self._is_open

    def connect(self):
        self._is_open = True
        if MockSerialConnection.is_demo:
            self._timer = threading.Timer(1, self._post_to_serial_connection)
            self._timer.start()
        return True

    @staticmethod
    def is_checksum_valid(remaining_bytes):
        check_sum_in_packet = MockSerialConnection._checksum_unpacker.unpack(
            remaining_bytes[len(remaining_bytes) - 2:len(remaining_bytes)])[0]
        calculated_checksum = sum([int(byte) for byte in remaining_bytes[0:len(
            remaining_bytes) - 2]])
        return check_sum_in_packet == calculated_checksum

    def receive(self):
        if not self.is_connected():
            raise RuntimeError("Serial connection not started!")
        while not self._fake_data:
            if self._cancel_read:
                return (0, 0, 0, 0, 0, 0, 0), []
        with self._fake_data_lock:
            data = self._fake_data.popleft()
        (PS, PL, DID, VER, PN, CH,
         PT) = MockSerialConnection._header_unpacker.unpack(data[0:8])
        if PS != 0xA5C3:
            return (0, 0, 0, 0, 0, 0, 0), []
        if MockSerialConnection.is_checksum_valid(data):
            return (PS, PL, DID, VER, PN, CH,
                    PT), data[8:len(data) - 2]
        else:
            return (0, 0, 0, 0, 0, 0, 0), []

    def load_fake_data(self, data):
        with self._fake_data_lock:
            self._fake_data.appendleft(data)

    def cancel_read(self):
        self._cancel_read = True

    def _post_to_serial_connection(self):
        self.load_fake_data(MockSerialConnection._numeric_packet)
        self._timer = threading.Timer(1, self._post_to_serial_connection)
        self._timer.start()
