# Two-Class Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the four loose functions in `support.py` with a stateful `MD5Extractor` class in `extractor.py`, and simplify `pdfAnalysis.search()` to delegate all logic to it.

**Architecture:** `MD5Extractor` owns the full extraction pipeline — scanning a directory, reading PDFs, extracting MD5 hashes, and writing the CSV. `pdfAnalysis` instantiates it, validates input, and passes itself as the progress callback. The two files have zero shared state; communication is through the constructor and `run()`.

**Tech Stack:** Python 3, pypdf, PyQt5, csv, pytest

---

## File Map

| File | Action | Responsibility |
|------|--------|---------------|
| `extractor.py` | Create | `MD5Extractor` class — all PDF/CSV logic |
| `tests/test_extractor.py` | Create | Tests for `MD5Extractor` |
| `md5Extractor.py` | Modify | Simplified GUI; delegates to `MD5Extractor` |
| `support.py` | Delete | Replaced by `extractor.py` |
| `tests/test_support.py` | Delete | Replaced by `tests/test_extractor.py` |

---

## Task 1: Write first failing tests — `__init__` and `dir_exists`

**Files:**
- Create: `tests/test_extractor.py`

- [ ] **Step 1: Create `tests/test_extractor.py` with path setup and first two tests**

```python
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
```

- [ ] **Step 2: Run tests — expect ImportError**

```
pytest tests/test_extractor.py -v
```

Expected: `ModuleNotFoundError: No module named 'extractor'`

---

## Task 2: Implement `MD5Extractor.__init__` and `dir_exists`

**Files:**
- Create: `extractor.py`

- [ ] **Step 1: Create `extractor.py` with class skeleton and `dir_exists`**

```python
import csv
import os
import re
import fnmatch
import pypdf


class MD5Extractor:
    MD5_PATTERN = r'[a-fA-F0-9]{32}'

    def __init__(self, directory, save_path):
        self.directory = directory
        self.save_path = save_path
        self.results = {}

    def dir_exists(self):
        return os.path.isdir(self.directory)
```

- [ ] **Step 2: Run tests — expect PASS**

```
pytest tests/test_extractor.py -v
```

Expected: `2 passed`

- [ ] **Step 3: Commit**

```
git add extractor.py tests/test_extractor.py
git commit -m "feat: add MD5Extractor skeleton with dir_exists"
```

---

## Task 3: TDD — `read_dir`

**Files:**
- Modify: `tests/test_extractor.py` (append)
- Modify: `extractor.py` (append method)

- [ ] **Step 1: Append two tests to `tests/test_extractor.py`**

```python
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
```

- [ ] **Step 2: Run — expect AttributeError**

```
pytest tests/test_extractor.py -v
```

Expected: `AttributeError: 'MD5Extractor' object has no attribute 'read_dir'`

- [ ] **Step 3: Add `read_dir` to `extractor.py`**

```python
    def read_dir(self):
        paths = []
        for root, _, files in os.walk(self.directory):
            for filename in fnmatch.filter(files, '*.pdf'):
                paths.append(os.path.join(root, filename))
        return paths
```

- [ ] **Step 4: Run — expect PASS**

```
pytest tests/test_extractor.py -v
```

Expected: `4 passed`

- [ ] **Step 5: Commit**

```
git add extractor.py tests/test_extractor.py
git commit -m "feat: add MD5Extractor.read_dir"
```

---

## Task 4: TDD — `get_pdf_content`

**Files:**
- Modify: `tests/test_extractor.py` (append)
- Modify: `extractor.py` (append method)

- [ ] **Step 1: Append tests to `tests/test_extractor.py`**

```python
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
```

- [ ] **Step 2: Run — expect AttributeError**

```
pytest tests/test_extractor.py -v
```

Expected: `AttributeError: 'MD5Extractor' object has no attribute 'get_pdf_content'`

- [ ] **Step 3: Add `get_pdf_content` to `extractor.py`**

```python
    def get_pdf_content(self, path):
        content = ""
        with open(path, "rb") as fh:
            pdf = pypdf.PdfReader(fh)
            for page in pdf.pages:
                content += (page.extract_text() or "") + "\n"
        return content
```

- [ ] **Step 4: Run — expect PASS**

```
pytest tests/test_extractor.py -v
```

Expected: `7 passed`

- [ ] **Step 5: Commit**

```
git add extractor.py tests/test_extractor.py
git commit -m "feat: add MD5Extractor.get_pdf_content"
```

---

## Task 5: TDD — `write_data`

**Files:**
- Modify: `tests/test_extractor.py` (append)
- Modify: `extractor.py` (append method)

- [ ] **Step 1: Append tests to `tests/test_extractor.py`**

```python
def test_write_data_writes_header_and_rows(tmp_path):
    out = str(tmp_path / "out.csv")
    ext = MD5Extractor(".", out)
    ext.results["a.pdf"] = {"d41d8cd98f00b204e9800998ecf8427e"}
    ext.write_data()

    with open(out, newline="") as fh:
        rows = list(csv.reader(fh))

    assert rows[0] == ["Absolute_Path", "MD5_Hash_Values"]
    assert ["a.pdf", "d41d8cd98f00b204e9800998ecf8427e"] in rows


def test_write_data_empty_results_writes_only_header(tmp_path):
    out = str(tmp_path / "empty.csv")
    ext = MD5Extractor(".", out)
    ext.write_data()

    with open(out, newline="") as fh:
        rows = list(csv.reader(fh))

    assert rows == [["Absolute_Path", "MD5_Hash_Values"]]
```

- [ ] **Step 2: Run — expect AttributeError**

```
pytest tests/test_extractor.py -v
```

Expected: `AttributeError: 'MD5Extractor' object has no attribute 'write_data'`

- [ ] **Step 3: Add `write_data` to `extractor.py`**

```python
    def write_data(self):
        with open(self.save_path, mode='a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Absolute_Path', 'MD5_Hash_Values'])
            for pdf, md5s in self.results.items():
                for md5 in md5s:
                    writer.writerow([pdf, md5])
```

- [ ] **Step 4: Run — expect PASS**

```
pytest tests/test_extractor.py -v
```

Expected: `9 passed`

- [ ] **Step 5: Commit**

```
git add extractor.py tests/test_extractor.py
git commit -m "feat: add MD5Extractor.write_data"
```

---

## Task 6: TDD — `run`

**Files:**
- Modify: `tests/test_extractor.py` (append)
- Modify: `extractor.py` (append method)

- [ ] **Step 1: Append tests to `tests/test_extractor.py`**

```python
def test_run_calls_progress_callback_and_produces_csv(tmp_path):
    shutil.copy(TESTPDF, tmp_path / "test.pdf")
    out = str(tmp_path / "output.csv")
    ext = MD5Extractor(str(tmp_path), out)
    callbacks = []
    ext.run(progress_callback=lambda c, t: callbacks.append((c, t)))
    assert os.path.exists(out)
    assert callbacks == [(1, 1)]


def test_run_without_callback_does_not_raise(tmp_path):
    shutil.copy(TESTPDF, tmp_path / "test.pdf")
    out = str(tmp_path / "output.csv")
    ext = MD5Extractor(str(tmp_path), out)
    ext.run()
    assert os.path.exists(out)


def test_run_end_to_end_finds_md5s(tmp_path):
    shutil.copy(TESTPDF, tmp_path / "test.pdf")
    out = str(tmp_path / "output.csv")
    ext = MD5Extractor(str(tmp_path), out)
    ext.run()

    with open(out, newline="") as fh:
        rows = list(csv.reader(fh))

    assert rows[0] == ["Absolute_Path", "MD5_Hash_Values"]
    assert len(rows) > 1
    assert all(MD5_RE.fullmatch(row[1]) for row in rows[1:])
```

- [ ] **Step 2: Run — expect AttributeError**

```
pytest tests/test_extractor.py -v
```

Expected: `AttributeError: 'MD5Extractor' object has no attribute 'run'`

- [ ] **Step 3: Add `run` to `extractor.py`**

```python
    def run(self, progress_callback=None):
        pdf_list = self.read_dir()
        total = len(pdf_list)
        for count, pdf in enumerate(pdf_list, 1):
            try:
                content = self.get_pdf_content(pdf)
                self.results[pdf] = set(re.findall(self.MD5_PATTERN, content))
            except Exception:
                pass
            if progress_callback:
                progress_callback(count, total)
        self.write_data()
```

- [ ] **Step 4: Run — expect PASS**

```
pytest tests/test_extractor.py -v
```

Expected: `12 passed`

- [ ] **Step 5: Commit**

```
git add extractor.py tests/test_extractor.py
git commit -m "feat: add MD5Extractor.run — full extraction pipeline"
```

---

## Task 7: Update `md5Extractor.py`

**Files:**
- Modify: `md5Extractor.py`

- [ ] **Step 1: Replace the imports at the top of `md5Extractor.py`**

Replace:
```python
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import support
import sys
import re
from collections import defaultdict
```

With:
```python
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from extractor import MD5Extractor
import sys
```

- [ ] **Step 2: Replace the `search` method body**

Replace the entire `search` method with:
```python
def search(self):
    dir = self.dir.text()
    save_location = self.save_location.text()
    extractor = MD5Extractor(dir, save_location)
    if not extractor.dir_exists():
        QMessageBox.warning(self, "Whoa dog!", "The PDF input directory does not exist")
        return
    extractor.run(progress_callback=self.report)
    exit()
```

- [ ] **Step 3: Update the `report` method signature to match the callback contract**

The existing signature `report(self, numsofar, listSize)` already matches `progress_callback(count, total)` — no change needed. Verify it reads:
```python
def report(self, numsofar, listSize):
    if listSize > 0:
        percent = numsofar * 100 / listSize
        self.progress.setValue(int(percent))
```

- [ ] **Step 4: Run the full test suite to confirm nothing broke**

```
pytest tests/test_extractor.py -v
```

Expected: `12 passed`

- [ ] **Step 5: Commit**

```
git add md5Extractor.py
git commit -m "refactor: simplify pdfAnalysis.search to delegate to MD5Extractor"
```

---

## Task 8: Delete `support.py` and `test_support.py`

**Files:**
- Delete: `support.py`
- Delete: `tests/test_support.py`

- [ ] **Step 1: Delete both files**

```
git rm support.py tests/test_support.py
```

- [ ] **Step 2: Run the full test suite — confirm all tests still pass**

```
pytest tests/test_extractor.py -v
```

Expected: `12 passed`

- [ ] **Step 3: Commit**

```
git commit -m "chore: remove support.py and test_support.py (replaced by extractor.py)"
```

---

## Done

The refactor is complete. `extractor.py` owns all extraction logic as a proper class with 12 passing tests. `md5Extractor.py` is a clean GUI layer with no embedded business logic.
