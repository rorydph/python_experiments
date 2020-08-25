import unittest
from pathlib import Path

class TestStringMethods(unittest.TestCase):

    # compare a generated file against a reference file
    def test_files(self):
        self.maxDiff = None
        gen = Path('./gen_file.param').read_text()
        ref = Path('./ref_file.param').read_text()
        self.assertMultiLineEqual(gen, ref)


if __name__ == '__main__':
    unittest.main()
