import serial
import struct


class SerialConnection:
    _header_unpacker = struct.Struct('H 6B')
    _HEADER_SIZE = 8
    _checksum_unpacker = struct.Struct('H')

    def __init__(self, usb_port):
        self._usb_port = usb_port
        self._serial_port = serial.Serial(self._usb_port, 9600)

    def is_connected(self):
        return self._serial_port.is_open

    def connect(self):
        if self.is_connected():
            return True
        self._serial_port.open()
        return self.isConnected

    @staticmethod
    def is_checksum_valid(remaining_bytes):
        check_sum_in_packet = SerialConnection._checksum_unpacker.unpack(
            remaining_bytes[len(remaining_bytes) - 2:len(remaining_bytes)])[0]
        calculated_checksum = sum([int(byte) for byte in remaining_bytes[0:len(
            remaining_bytes) - 2]])
        return check_sum_in_packet == calculated_checksum

    def receive(self):
        header = self._serial_port.read(self._HEADER_SIZE)
        if len(header) < self._HEADER_SIZE:
            return (0, 0, 0, 0, 0, 0, 0), []
        (PS, PL, DID, VER, PN, CH,
         PT) = SerialConnection._header_unpacker.unpack(header)
        if PS != 0xA5C3:
            # clear the potential bad packets from the input buffer
            self._serial_port.reset_input_buffer()
            return (0, 0, 0, 0, 0, 0, 0), []
        remaining_bytes_len = PL - self._HEADER_SIZE
        remaining_bytes = self._serial_port.read(remaining_bytes_len)

        if SerialConnection.is_checksum_valid(header + remaining_bytes):
            return (PS, PL, DID, VER, PN, CH, PT), remaining_bytes[
                                                   0:len(remaining_bytes) - 2]
        else:
            # clear the potential bad packets from the input buffer
            print(PT)
            self._serial_port.reset_input_buffer()
            return (0, 0, 0, 0, 0, 0, 0), []

    def cancel_read(self):
        self._serial_port.cancel_read()
