# md5Extractor

`md5Extractor` is a small PyQt5 desktop tool that scans PDF files for MD5-shaped hash values and writes the results to a text file named `md5Output.txt`.

The app recursively searches a selected PDF directory for `*.pdf` files, extracts page text with `pypdf`, finds 32-character hexadecimal strings, and writes one output row per PDF/hash pair.

## Features

- PyQt5 GUI with separate buttons for selecting:
  - the directory containing PDFs to parse
  - the output directory for the results file
- Recursive PDF discovery.
- PDF text extraction through `pypdf`.
- MD5-pattern matching with `[a-fA-F0-9]{32}`.
- Duplicate hash values are collapsed per PDF.
- Automatic output directory creation when the directory does not already exist.
- Fixed output filename: `md5Output.txt`.
- Progress bar updates as PDFs are processed.

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

- `Browse PDFs`: select the folder containing the PDFs to scan.
- `Output Folder`: select the folder where `md5Output.txt` should be written.
- `Execute`: start extraction.

You can also type paths directly into the text fields. If the output folder does not exist, the program attempts to create it before writing the output file.

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

The file content uses CSV-style rows:

```csv
Absolute_Path,MD5_Hash_Values
C:\path\to\file.pdf,44d88612fea8a8f36de82e1278abb02f
```

Each row contains:

- `Absolute_Path`: the PDF where the hash was found.
- `MD5_Hash_Values`: one matched 32-character hexadecimal value.

If a PDF contains more than one unique matching hash, each hash is written on its own row. If the same hash appears multiple times in the same PDF, it is written once for that PDF.

## Important Behavior

- The app matches MD5-shaped strings. It does not verify that a value is actually the MD5 hash of a file.
- PDFs that cannot be read are skipped.
- Existing `md5Output.txt` files are appended to because the writer currently opens the file in append mode.
- Each run writes a header row before writing results.
- The GUI exits after extraction completes.

## Project Layout

```text
md5Extractor.py      PyQt5 GUI entry point
extractor.py         PDF scanning, hash extraction, and output writing
requirements.txt     Runtime dependencies
testpdf.pdf          Sample PDF fixture
README.md            Current documentation
README.txt           Legacy documentation
contributors.txt     Contributor information
```

## Implementation Notes

The main extraction class is `MD5Extractor` in `extractor.py`.

Key methods:

- `dir_exists()` checks whether the PDF input directory exists.
- `read_dir()` recursively finds PDF files.
- `get_pdf_content()` extracts text from a PDF.
- `extract()` coordinates scanning, matching, progress updates, and output writing.
- `write_data()` writes results to `md5Output.txt`.

The GUI in `md5Extractor.py` builds the final output path by joining the selected output directory with `md5Output.txt`.

## Development Validation

Run syntax validation after changing Python files:

```powershell
python -m py_compile md5Extractor.py extractor.py
```

If tests are added or restored, run:

```powershell
python -m pytest
```
