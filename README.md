# md5Extractor

Date:  2/27/2015

`md5Extractor` is a small Python GUI tool for scanning PDF files in a directory and writing any MD5-looking hash values it finds to a CSV file.

The application recursively searches for `*.pdf` files, extracts text from each PDF with `pypdf`, finds 32-character hexadecimal strings, and writes the results in this format:

```csv
Absolute_Path,MD5_Hash_Values
C:\path\to\file.pdf,44d88612fea8a8f36de82e1278abb02f
```

## Features

- PyQt5 desktop interface.
- Recursive PDF discovery.
- Text extraction from PDF pages.
- MD5-pattern matching with the regex `[a-fA-F0-9]{32}`.
- Duplicate hashes are collapsed per PDF.
- CSV output with one row per PDF/hash pair.
- Automated tests for the extractor behavior.

## Project Layout

```text
md5Extractor.py        PyQt5 GUI entry point
extractor.py           MD5Extractor implementation
requirements.txt       Runtime dependencies
tests/test_extractor.py
                       Extractor tests
testpdf.pdf            Test fixture used by the test suite
README.txt             Legacy README
README.md              Current project documentation
```

## Requirements

- Python 3
- `pypdf`
- `PyQt5`
- `pytest` if you want to run tests

Install the runtime dependencies from the project root:

```powershell
python -m pip install -r requirements.txt
```

Install `pytest` if it is not already available:

```powershell
python -m pip install pytest
```

## Running the App

From the project directory:

```powershell
cd C:\data\projects\md5Extractor
python md5Extractor.py
```

The GUI has two text fields and two buttons:

1. Enter the directory containing PDFs in the first field.
2. Click `Browse` and choose the CSV output file path.
3. Click `Execute`.

When extraction finishes, the app writes the CSV file and exits.

## Output Format

The output file is written as CSV with this header:

```csv
Absolute_Path,MD5_Hash_Values
```

Each following row contains:

- `Absolute_Path`: path to the PDF file where the hash was found.
- `MD5_Hash_Values`: one matched 32-character hexadecimal value.

If a PDF contains multiple unique matching hashes, the CSV contains one row per hash. If the same hash appears multiple times in a PDF, it is written once for that PDF.

## Running Tests

From the project directory:

```powershell
python -m pytest
```

The tests verify:

- directory existence checks
- recursive PDF discovery
- PDF text extraction
- MD5 pattern matching from the test PDF fixture
- end-to-end extraction and CSV writing

## Implementation Notes

The main extraction logic lives in `extractor.py`:

- `MD5Extractor.dir_exists()` checks whether the configured input directory exists.
- `MD5Extractor.read_dir()` recursively finds PDF files.
- `MD5Extractor.get_pdf_content()` extracts text from a PDF.
- `MD5Extractor.extract()` coordinates scanning, matching, progress updates, and CSV writing.
- `MD5Extractor.write_data()` writes the current results to CSV.

The GUI in `md5Extractor.py` creates an `MD5Extractor` instance and passes the progress bar's `setValue` method as the progress callback.

## Known Behavior

- The app matches MD5-shaped strings only. It does not verify that the values are known file hashes.
- PDF files that cannot be read are skipped.
- The CSV file is opened in append mode, so repeated runs against the same output file add another header and additional rows.
- The current GUI exits after a completed extraction.

## Development

Before changing extraction behavior, run:

```powershell
python -m pytest
python -m py_compile md5Extractor.py extractor.py
```

Keep changes focused on the existing architecture unless a larger redesign is intentional.
