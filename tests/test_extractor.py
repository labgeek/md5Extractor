import os
import re
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


def test_read_dir_finds_pdfs(tmp_path):
    (tmp_path / "a.pdf").write_bytes(b"")
    (tmp_path / "b.txt").write_bytes(b"")
    ext = MD5Extractor(str(tmp_path), "out.csv")
    result = ext.read_dir()
    assert len(result) == 1
    assert result[0].endswith("a.pdf")


def test_read_dir_empty_when_no_pdfs(tmp_path):
    ext = MD5Extractor(str(tmp_path), "out.csv")
    assert ext.read_dir() == []


def test_testpdf_fixture_exists():
    assert os.path.isfile(TESTPDF), "testpdf.pdf is required for extraction tests"


def test_get_pdf_content_returns_nonempty_string():
    ext = MD5Extractor(".", "out.csv")
    content = ext.get_pdf_content(TESTPDF)
    assert isinstance(content, str)
    assert len(content) > 0


def test_get_pdf_content_finds_md5_hashes():
    ext = MD5Extractor(".", "out.csv")
    content = ext.get_pdf_content(TESTPDF)
    md5s = MD5_RE.findall(content)
    assert len(md5s) > 0, "expected at least one MD5 hash in the test PDF"
