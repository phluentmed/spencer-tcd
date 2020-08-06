from Components.HTTPExporter import HTTPExporter
from Components.MockRequests import MockRequests

import time
import unittest


class HTTPExporterTests(unittest.TestCase):
    # TODO see if theres a setup before run test suite
    def test_breathing(self):
        MockRequests.load_host("localhost")
        http_exporter = HTTPExporter("localhost", MockRequests)
        result = http_exporter.start()
        self.assertEqual(result, 0)
        result = http_exporter.stop()
        self.assertEqual(result, 0)

    def test_export_returns_success_code(self):
        MockRequests.load_host("localhost")
        http_exporter = HTTPExporter("localhost", MockRequests)
        http_exporter.start()
        result = http_exporter.export("BigData", None)
        self.assertEqual(result, 0)
        http_exporter.stop()

    def test_no_start_stop_returns_failure_code(self):
        MockRequests.load_host("localhost")
        http_exporter = HTTPExporter("localhost", MockRequests)
        result = http_exporter.stop()
        self.assertEqual(result, -1)

    def test_double_start_returns_failure_code(self):
        MockRequests.load_host("localhost")
        http_exporter = HTTPExporter("localhost", MockRequests)
        http_exporter.start()
        result = http_exporter.start()
        self.assertEqual(result, -1)
        http_exporter.stop()

    def test_invalid_host_returns_failure_code(self):
        MockRequests.load_host("localhost")
        http_exporter = HTTPExporter("bogusHost", MockRequests)
        result = http_exporter.start()
        self.assertEqual(result, 0)
        http_exporter.export("BioData", None)
        time.sleep(3)
        self.assertEqual(MockRequests._last_response.status_code, 400)
        http_exporter.stop()
