from Components.CSVExporter import CSVExporter
import csv
import os
import random
import shutil
import string
import unittest


def generateDictionaryData():
    numbers = string.digits
    letters = string.ascii_uppercase
    hexdigits = string.hexdigits
    return {'number': ''.join(random.choice(numbers) for i in range(10)),
            'hex': ''.join(random.choice(hexdigits) for i in range(10)),
            'letters': ''.join(random.choice(letters) for i in range(10))}


def result_handler(*args):
    pass


test_dir = 'TestArtifacts'
test_file = test_dir + '/' + 'test_file.csv'


class CSVExporterTests(unittest.TestCase):

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

    def test_breathing(self):
        csv_exporter = CSVExporter(test_file)
        result = csv_exporter.start()
        self.assertEqual(result, 0)
        result = csv_exporter.stop(result_handler)
        self.assertEqual(result, 0)

    def test_write_no_start(self):
        csv_exporter = CSVExporter(test_file)
        result = csv_exporter.export(generateDictionaryData(), result_handler)
        self.assertEqual(result, -1)
        csv_exporter.start()
        csv_exporter.stop(result_handler)
        result = csv_exporter.export(generateDictionaryData(), result_handler)
        self.assertEqual(result, -1)

    def test_write_one_export(self):
        csv_exporter = CSVExporter(test_file, 1)
        csv_exporter.start()
        data = generateDictionaryData()
        csv_exporter.export(data, result_handler)
        csv_exporter.stop(result_handler)
        with open(test_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            it = iter(reader)
            result = dict(next(it))
            self.assertDictEqual(data, result)

    def test_multiple_exports(self):
        csv_exporter = CSVExporter(test_file, 5)
        csv_exporter.start()
        data = []
        for i in range(0, 5):
            data.append(generateDictionaryData())
            csv_exporter.export(data[i], result_handler)
        csv_exporter.stop(result_handler)
        with open(test_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result = dict(row)
                self.assertTrue(data)
                self.assertDictEqual(data[0], result)
                data.pop(0)
            self.assertFalse(data)

    def test_buffer_naggling_flush(self):
        csv_exporter = CSVExporter(test_file, 3)
        data = []
        csv_exporter.start()
        for i in range(0, 2):
            data.append(generateDictionaryData())
            csv_exporter.export(data[i], result_handler)
        self.assertFalse(os.path.isfile(test_file))
        csv_exporter.stop(result_handler)
        with open(test_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result = dict(row)
                self.assertTrue(data)
                self.assertDictEqual(data[0], result)
                data.pop(0)
            self.assertFalse(data)

    def test_naggling_double_file_open_close(self):
        csv_exporter = CSVExporter(test_file, 2)
        data = []
        csv_exporter.start()
        for i in range(0, 4):
            data.append(generateDictionaryData())
            csv_exporter.export(data[i], result_handler)
        csv_exporter.stop(result_handler)
        with open(test_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result = dict(row)
                self.assertTrue(data)
                self.assertDictEqual(data[0], result)
                data.pop(0)
            self.assertFalse(data)
