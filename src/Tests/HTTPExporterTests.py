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

    def test_export(self):
        pass

    def test_no_start_stop(self):
        pass

    def test_double_start(self):
        pass

    def test_invalid_host(self):
        httpExporter = HTTPExporter("bogusHost")
        result = httpExporter.start()
        self.assertEqual(result, 0)
        with self.assertRaises(requests.exceptions.MissingSchema):
            httpExporter.export("BioData", None)

