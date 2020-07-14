import unittest
from Components.SerialConnection import SerialConnection


class TestChecksums(unittest.TestCase):
    # commented out version is for windows
    correct_packet = b'\xc3\xa50\xd1\x03\xe5\x01\x02\xd7\xfa\xcf4i\x01\x00' \
                     b'\x00\x01\x00       ' \
                     b'\x00\x002\n\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                     b'\x00\x00\x00\x00\x00\x00\x00\xb5\x07'

    # correct_packet = [195, 165, 48, 209, 3, 229, 1, 2, 215, 250, 207, 52,
    # 105, 1, 0, 0, 1, 0, 32, 32, 32, 32, 32, 32, 32, 0, 0, 50, 10, 6, 0, 0,
    # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 181, 7]
    incorrect_packet = b'\xc3\xa50\xd1\x03\xe5\x01\x02\xd7\xfa\xcf4i\x01\x00' \
                       b'\x00\x01\x00       ' \
                       b'\x00\x002\n\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                       b'\x00\x00\x00\x00\x00\x00\x00\xb5c'

    # incorrect_packet = [195, 165, 48, 209, 3, 229, 1, 2, 215, 250, 207,
    # 52, 105, 1, 0, 0, 1, 0, 32, 32, 32, 32, 32, 32, 32, 0, 0, 50, 10, 6,
    # 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 181, 99]

    def test_checksum_correct(self):
        self.assertTrue(
            SerialConnection.is_checksum_valid(self.correct_packet))

    def test_checksum_incorrect(self):
        self.assertFalse(
            SerialConnection.is_checksum_valid(self.incorrect_packet))
