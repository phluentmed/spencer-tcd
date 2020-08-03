from Components.HTTPExporter import HTTPExporter

import requests
import unittest

class HTTPExporterTests(unittest.TestCase):

    def test_breathing(self):
        httpExporter = HTTPExporter("localhost")
        result = httpExporter.start()
        self.assertEqual(result, 0)
        result = httpExporter.stop()
        self.assertEqual(result, 0)

    def test_export_returns_success_code(self):
        httpExporter = HTTPExporter("localhost")
        httpExporter.start()
        result = httpExporter.export("BigData", None)
        self.assertEqual(result, 0)

    def test_no_start_stop_returns_failure_code(self):
        httpExporter = HTTPExporter("localhost")
        result = httpExporter.stop()
        self.assertEqual(result, -1)

    def test_double_start_returns_failure_code(self):
        httpExporter = HTTPExporter("localhost")
        httpExporter.start()
        result = httpExporter.start()
        self.assertEqual(result, -1)

    def test_invalid_host_returns_failure_code(self):
        httpExporter = HTTPExporter("http://bogusHost")
        result = httpExporter.start()
        self.assertEqual(result, 0)
        result = httpExporter.export("BioData", None)
        self.assertEqual(result, -1)