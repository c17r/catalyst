import unittest
import subprocess
import os
import mountains


class CatalystTest(unittest.TestCase):

    def test_get_data(self):
        filename = "mountains-1.csv"

        expected = self.get_input_file(filename)
        actual = mountains.get_data(filename)

        self.assert_list(expected, actual)

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
