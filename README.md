# MD5Extractor

Author: labgeek@gmail.com (JD Durick)

`MD5Extractor` is a PyQt5 desktop application that scans PDF files for MD5-shaped hash values and writes the results to `md5Output.txt`.

The app recursively searches a selected input folder for PDF files, extracts page text with `pypdf`, finds 32-character hexadecimal values, and writes one row per PDF/hash pair.

## Features

- Branded PyQt5 interface with the application title, version, author, and current launch date.
- Input folder picker for the PDF directory.
- Output folder picker for the generated `md5Output.txt` file.
- Threaded PDF scanning so the GUI remains responsive during extraction.
- Progress bar that updates as PDFs are processed.
- Results table with separate columns for:
  - PDF file path
  - MD5 hash value
- Scan summary showing:
  - PDFs scanned
  - hashes found
  - skipped files
  - output file path
- Read-only output path field with copy support and tooltip for long paths.
- Clear Form button to reset inputs, results, progress, and summary data.
- README button that opens or closes this README in a separate read-only window.
- Professional validation messages for input, output, and scan errors.
- Duplicate hash values are collapsed per PDF.
- Output directory creation when the selected output directory does not already exist.

## Requirements

- Python 3
- `pypdf`
- `PyQt5`

Install dependencies from the project root:

```powershell
python -m pip install -r requirements.txt
```

## Running the App

From the project directory:

```powershell
cd C:\data\projects\md5Extractor
python md5Extractor.py
```

The application window provides:

- `Select Input Folder`: choose the folder containing PDFs to scan.
- `Select Output Folder`: choose where `md5Output.txt` should be written.
- `Start Scan`: begin scanning PDFs.
- `Clear Form`: clear the selected paths, results table, progress bar, and scan summary.
- `Open README`: open this README in a separate window. Click the button again to close it.

You can also type paths directly into the input fields.

## Output File

The output file is always named:

```text
md5Output.txt
```

It is written inside the selected output directory. For example, if the output directory is:

```text
C:\data\projects\md5Extractor\out
```

the final output path is:

```text
C:\data\projects\md5Extractor\out\md5Output.txt
```

The output uses CSV-style rows:

```csv
Absolute_Path,MD5_Hash_Values
C:\path\to\file.pdf,44d88612fea8a8f36de82e1278abb02f
```

Each row contains:

- `Absolute_Path`: the full path of the PDF where the hash was found.
- `MD5_Hash_Values`: one matched 32-character hexadecimal value.

If a PDF contains more than one unique matching hash, each hash is written on its own row. If the same hash appears multiple times in the same PDF, it is written once for that PDF.

## Important Behavior

- The app matches MD5-shaped strings. It does not verify that a value is actually the MD5 hash of a file.
- PDFs that cannot be read are skipped and counted in the scan summary.
- Existing `md5Output.txt` files are appended to because the writer opens the file in append mode.
- Each scan writes a header row before writing results.
- Scanning runs in a worker thread and controls are disabled during an active scan.
- The GUI remains open after extraction completes.
- Image-only or scanned PDFs may not produce text unless OCR is added separately.

## Project Layout

```text
md5Extractor.py      PyQt5 GUI entry point and README viewer
extractor.py         PDF scanning, hash extraction, and output writing
requirements.txt     Runtime dependencies
testpdf.pdf          Sample PDF fixture
README.md            Current documentation
contributors.txt     Contributor information
```

## Implementation Notes

The main extraction class is `MD5Extractor` in `extractor.py`.

Key methods:

- `dir_exists()` checks whether the PDF input directory exists.
- `read_dir()` recursively finds PDF files and returns them in sorted order.
- `get_pdf_content()` extracts text from a PDF.
- `extract()` coordinates scanning, matching, progress updates, status updates, result callbacks, and output writing.
- `write_data()` writes results to `md5Output.txt`.

The GUI in `md5Extractor.py`:

- builds the final output path by joining the selected output directory with `md5Output.txt`
- displays results in a table
- tracks scan progress and summary counts
- runs extraction through a `QThread` worker
- opens and closes `README.md` in a separate read-only window

## Development Validation

Run syntax validation after changing Python files:

```powershell
python -m py_compile md5Extractor.py extractor.py
```

If tests are added later, run the project test command documented with those tests.
