import sys
import pathlib
import unittest
from indicator import indicator

class test_indicator(unittest.TestCase):

    def test_indication_red(self):
        ind = indicator()
        result = ind.indication(3)
        self.assertEqual("red", result)

    def test_indication_yellow(self):
        ind = indicator()
        result = ind.indication(6)
        self.assertEqual("yellow", result)

    def test_indication_green(self):
        ind = indicator()
        result = ind.indication(11)
        self.assertEqual("green", result)

if __name__ == '__main__':
    unittest.main()