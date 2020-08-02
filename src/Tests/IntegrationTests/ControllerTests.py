from controller import Controller
from Components.MockSerialConnection import MockSerialConnection
import csv
import time
import timeout_decorator
import unittest
import os
import shutil

test_dir = 'TestArtifacts'
test_file = test_dir + '/' + 'test_file.csv'
numeric_packet = b'\xc3\xa50\xd1\x03\xe5\x01\x02\xd7\xfa\xcf4i\x01\x00' \
                 b'\x00\x01\x00       ' \
                 b'\x00\x002\n\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\xb5\x07'
numeric_packet_decoded = numeric_packet_output = {'Time': str(1551369239255),
                                                  'Channel': str(1),
                                                  'VesselLabel': str(
                                                      b'       \x00\x00'),
                                                  'Depth': str(50), 'Power': str(10),
                                                  'SampleRate': str(6),
                                                  'EmboliCount': str(0),
                                                  'PeakVelocity': str(0),
                                                  'DiastolicVelocity': str(0),
                                                  'MeanVelocity': str(0),
                                                  'EmboliRate': str(0)}


class ControllerTests(unittest.TestCase):

    def setUp(self):
        if not os.path.isdir(test_dir):
            try:
                os.mkdir(test_dir)
            except FileExistsError:
                print("Directory ", test_dir, " already exists")

    def tearDown(self):
        if os.path.isdir(test_dir):
            try:
                shutil.rmtree(test_dir)
            except OSError as err:
                print(err)

    @timeout_decorator.timeout(10, timeout_exception=TimeoutError)
    def test_breathing(self):
        controller = Controller(MockSerialConnection, 'test', test_file)
        self.assertEqual(controller.start(), 0)
        time.sleep(1)
        self.assertEqual(controller.stop(), 0)

    """
    Test to make sure none of the components are active before the controller
    is started.
    """
    def test_no_start(self):
        controller = Controller(MockSerialConnection, 'test', test_file)
        self.assertFalse(controller._serial_connection.is_connected())
        self.assertFalse(controller._data_handler_thread.is_alive())

    @timeout_decorator.timeout(10, timeout_exception=TimeoutError)
    def test_csv_export(self):
        self.maxDiff = None
        controller = Controller(MockSerialConnection, 'test', test_file)
        controller._serial_connection.load_fake_data(numeric_packet)
        controller._serial_connection.load_fake_data(numeric_packet)
        self.assertEqual(controller.start(), 0)
        time.sleep(3)
        self.assertEqual(controller.stop(), 0)
        with open(test_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result = dict(row)
                self.assertDictEqual(numeric_packet_decoded, result)