# TODO

Feature ideas and engineering improvements for future MD5Extractor releases.

## High Priority

- [ ] Add an output mode option:
  - overwrite existing `md5Output.txt`
  - append to existing `md5Output.txt`
  - prevent duplicate header rows when appending
- [ ] Add a `Cancel Scan` button for large PDF batches.
- [ ] Show current scan progress as file count, such as `Processing 12 of 100`.
- [ ] Add an error/skipped-files table with:
  - PDF path
  - failure reason
  - file count summary
- [ ] Improve MD5 matching so 32-character matches are not extracted from inside longer hexadecimal strings.

## Result Improvements

- [ ] Track and display the page number where each hash was found.
- [ ] Add surrounding text snippet/context for each match.
- [ ] Add duplicate count per PDF/hash pair.
- [ ] Add a search/filter box for the results table.
- [ ] Add copy options:
  - copy selected row
  - copy selected hash
  - copy all results
- [ ] Add a button to open the output folder after a scan.

## Hash Support

- [ ] Add selectable hash types:
  - MD5
  - SHA-1
  - SHA-256
  - SHA-512
- [ ] Add an `All supported hashes` scan mode.
- [ ] Add a `Hash Type` column to the results table and output file.

## PDF Handling

- [ ] Detect encrypted PDFs and report them separately.
- [ ] Detect image-only PDFs that do not contain extractable text.
- [ ] Continue scanning other pages if one page fails, instead of skipping the whole PDF.
- [ ] Consider optional OCR support for scanned PDFs.

## User Interface

- [ ] Add drag-and-drop support for PDF folders.
- [ ] Allow selecting individual PDF files in addition to folders.
- [ ] Remember the last used input and output directories.
- [ ] Add a recent folders menu.
- [ ] Add a menu bar with:
  - File
  - Help
  - About
- [ ] Add an About dialog with version, author, license, and GitHub URL.
- [ ] Add an application icon.

## Packaging and Release

- [ ] Add a repeatable build script for PyInstaller.
- [ ] Add GitHub release checklist documentation.
- [ ] Include `README.md` and sample assets in packaged builds.
- [ ] Add a Windows executable artifact to each GitHub release.
- [ ] Add version metadata to the Windows executable.

## Testing and Quality

- [ ] Add automated tests for `extractor.py`.
- [ ] Add tests for:
  - recursive PDF discovery
  - MD5 extraction
  - duplicate hash collapsing
  - skipped PDF tracking
  - output file writing
- [ ] Add a small test fixture with known hash values.
- [ ] Add linting or formatting checks.
- [ ] Add GitHub Actions CI for syntax checks and tests.

## Documentation

- [ ] Add updated screenshots of the current GUI.
- [ ] Add a release download section to `README.md`.
- [ ] Add build-from-source instructions.
- [ ] Add troubleshooting notes for PyInstaller and missing dependencies.
- [ ] Add a license file.
