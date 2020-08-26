import pytest, difflib
from pathlib import Path


def test_file_diff():
    gen = Path('gen_file.param').read_text()
    ref = Path('ref_file.param').read_text()
    assert gen == ref


if __name__ == '__main__':
    test_file_diff()
