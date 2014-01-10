import unittest
import subprocess
import os
import mountains
from datetime import datetime


class CatalystTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.url = "http://www.catalystsecure.com/public/tasks/mountains/mountains-1.csv"
        self.filename = "mountains-1.csv"
        self.local_lines = self.get_input_file(self.filename)
        self.expected_key = {
            "GeoNameId": 0,
            "Name": 1,
            "Country": 2,
            "Latitude": 3,
            "Longitude": 4,
            "Altitude (m)": 5
        }

        super(CatalystTest, self).__init__(*args, **kwargs)

    def test_get_file_data(self):
        actual = mountains.get_file_data(self.filename)

        self.assert_list(self.local_lines, actual)

    def test_get_http_data_1(self):
        url = "http://httpbin.org/get"
        data = mountains.get_http_data(url)

        found = False
        for line in data:
            if line.find('"url"') and line.find(url):
                found = True
                break

        self.assertTrue(found, "invalid returned HTTP data")

    def test_header_key(self):
        actual = mountains.create_key(self.local_lines[0])

        self.assertEqual(self.expected_key, actual)

    def test_header(self):
        expected = "2014-01-16 15:42:29 (Thursday)"

        dt = datetime(2014, 1, 16, 15, 42, 29)
        header = mountains.create_header(dt)
        actual = header.split(os.linesep)[0]

        self.assertEqual(expected, actual)

    def test_format_data_1(self):
        input = "5885171,Angel Peak,CA,58.48553,-124.85859,6858"
        expected = "Angel Peak has an altitude of 6858 meters."
        actual = mountains.format_data(self.expected_key, input)

        self.assertEqual(expected, actual)

    def test_format_data_2(self):
        input = "6115068,Queen Charlotte Island,CA,52.9995,-132.0034,null"
        expected = "Queen Charlotte Island has an altitude of unknown meters."
        actual = mountains.format_data(self.expected_key, input)

        self.assertEqual(expected, actual)

    def test_full_output(self):
        expected = self.get_expected_output()
        actual = self.get_actual_output()

        self.assert_list(expected, actual)

    def get_input_file(self, filename):
        lines = [l.rstrip() for l in open(filename, "r")]
        return lines

    def get_expected_output(self):
        lines = self.get_input_file("mountains-1.expected")
        del lines[0]
        return lines

    def get_actual_output(self):
        output = subprocess.check_output(["python", "./mountains.py", self.url])
        output_lines = output.split(os.linesep)
        del output_lines[0]
        return output_lines

    def assert_list(self, expected, actual):
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

if __name__ == "__main__":
    unittest.main()
