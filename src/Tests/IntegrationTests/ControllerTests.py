from controller import Controller
from Components.MockSerialConnection import MockSerialConnection
import time
import timeout_decorator
import unittest

test_dir = 'TestArtifacts'
test_file = test_dir + '/' + 'test_file.csv'
numeric_packet = b'\xc3\xa50\xd1\x03\xe5\x01\x02\xd7\xfa\xcf4i\x01\x00' \
                 b'\x00\x01\x00       ' \
                 b'\x00\x002\n\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
                 b'\x00\x00\x00\x00\x00\x00\x00\xb5\x07'


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