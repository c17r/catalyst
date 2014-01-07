import unittest
import subprocess
import os
import mountains
from datetime import datetime


class CatalystTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.filename = "mountains-1.csv"
        self.local_lines = self.get_input_file(self.filename)

        super(CatalystTest, self).__init__(*args, **kwargs)

    def test_get_data(self):
        actual = mountains.get_data(self.filename)

        self.assert_list(self.local_lines, actual)

    def test_header_key(self):
        expected = {
            "GeoNameId": 0,
            "Name": 1,
            "Country": 2,
            "Latitude": 3,
            "Longitude": 4,
            "Altitude (m)": 5
        }
        actual = mountains.create_key(self.local_lines[0])

        self.assertEqual(expected, actual)

    def test_header(self):
        expected = "2014-01-16 15:42:29 (Thursday)"

        dt = datetime(2014, 1, 16, 15, 42, 29)
        header = mountains.create_header(dt)
        actual = header.split(os.linesep)[0]

        self.assertEqual(expected, actual)

    def test_output(self):
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
        output = subprocess.check_output(["python", "./mountains.py"])
        output_lines = output.split(os.linesep)
        del output_lines[0]
        return output_lines

    def assert_list(self, expected, actual):
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

if __name__ == "__main__":
    unittest.main()
