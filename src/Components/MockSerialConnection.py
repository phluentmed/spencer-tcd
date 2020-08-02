from collections import deque
from Components.SerialConnection import SerialConnection
import struct
import threading


class MockSerialConnection(SerialConnection):
    _header_unpacker = struct.Struct('H 6B')
    _HEADER_SIZE = 8
    _checksum_unpacker = struct.Struct('H')

    def __init__(self,
                 usb_port,
                 serial_connect_fail=False,
                 check_sum_fail=False):
        self._usb_port = usb_port
        self._is_open = False
        self._serial_connect_fail = serial_connect_fail
        self._checksum_fail = check_sum_fail
        self._fake_data = deque()
        self._fake_data_lock = threading.RLock()
        self._cancel_read = False

    def is_connected(self):
        return self._is_open

    def connect(self):
        if self._serial_connect_fail:
            return False
        self._is_open = True
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
        data = object
        while not self._fake_data:
            if self._cancel_read:
                return (0, 0, 0, 0, 0, 0, 0), []
        with self._fake_data_lock:
            data = self._fake_data.popleft()
        (PS, PL, DID, VER, PN, CH,
         PT) = MockSerialConnection._header_unpacker.unpack(data[0:8])
        if PS != 0xA5C3:
            return (0, 0, 0, 0, 0, 0, 0), []
        if self._checksum_fail:
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
