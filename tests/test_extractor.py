import csv
import os
import re
import shutil
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from extractor import MD5Extractor  # noqa: E402

TESTPDF = os.path.join(ROOT, "testpdf.pdf")
MD5_RE = re.compile(r'[a-fA-F0-9]{32}')


def test_dir_exists_true_for_real_dir():
    ext = MD5Extractor(ROOT, "out.csv")
    assert ext.dir_exists() is True


def test_dir_exists_false_for_missing_dir():
    ext = MD5Extractor(os.path.join(ROOT, "definitely-not-here"), "out.csv")
    assert ext.dir_exists() is False
