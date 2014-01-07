import unittest, subprocess, os

class CatalystTest(unittest.TestCase):

    def test_output(self):
        expected = self.get_expected()
        actual = self.get_actual()

        for e, a in zip(expected, actual):
            self.assertEqual(e, a)

    def get_expected(self):
        lines = [l.rstrip() for l in open("mountains-1.expected", "r")]
        del lines[0]
        return lines

    def get_actual(self):
        output = subprocess.check_output(["python", "./mountains.py"])
        output_lines = output.split(os.linesep)
        del output_lines[0]
        return output_lines

if __name__ == "__main__":
    unittest.main()