# Design: Two-Class Refactor

**Date:** 2026-06-09  
**Status:** Approved

## Goal

Improve code organization by introducing a proper class-based structure across two files, separating business logic from the GUI layer.

## Current State

- `md5Extractor.py` — PyQt5 GUI class (`pdfAnalysis`) that mixes UI logic with PDF processing and MD5 extraction
- `support.py` — Four loose utility functions with no class structure

## Proposed Structure

### `extractor.py` — `MD5Extractor` class

Replaces `support.py`. Encapsulates all PDF processing and MD5 extraction logic as a stateful class.

**Constructor:** `MD5Extractor(directory, save_path)`
- `self.directory` — input directory path
- `self.save_path` — output CSV path
- `self.results` — `defaultdict(list)` holding extracted MD5s keyed by PDF path

**Methods:**
- `dir_exists() → bool` — validates that `self.directory` exists on disk
- `read_dir() → list[str]` — walks `self.directory` recursively, returns paths of all `.pdf` files
- `get_pdf_content(path: str) → str` — opens a single PDF and returns all page text concatenated
- `run(progress_callback=None)` — orchestrates the full extraction: scans dir, extracts MD5s via regex into `self.results`, calls `progress_callback(count, total)` if provided, then calls `write_data()`
- `write_data()` — writes `self.results` to a CSV at `self.save_path` with columns `Absolute_Path`, `MD5_Hash_Values`

### `md5Extractor.py` — `pdfAnalysis` class (simplified)

GUI class is unchanged structurally. The `search()` method is simplified:

1. Instantiates `MD5Extractor(dir, save_location)`
2. Calls `extractor.dir_exists()` for input validation (shows warning dialog on failure)
3. Calls `extractor.run(progress_callback=self.report)`
4. All inline regex, dict, and CSV logic is removed from this file

**Cleanup:** bare `except: pass` tightened to `except Exception: pass`.

The `report(count, total)` method stays as-is and becomes the progress callback passed to `run()`.

Entry point (`if __name__ == "__main__"`) is unchanged.

## Data Flow

```
pdfAnalysis.search()
  → MD5Extractor(dir, save_path)
  → extractor.dir_exists()          # validate input
  → extractor.run(self.report)
      → read_dir()                  # collect PDF paths
      → for each pdf:
          get_pdf_content(pdf)      # extract text
          re.findall(md5_pattern)   # find MD5s
          self.results[pdf] = md5s  # store
          progress_callback(n, total)
      → write_data()                # write CSV
```

## File Changes

| File | Action |
|------|--------|
| `support.py` | Deleted (replaced by `extractor.py`) |
| `extractor.py` | New — contains `MD5Extractor` class |
| `md5Extractor.py` | Modified — `import extractor`, simplified `search()` |

## Out of Scope

- No GUI changes beyond wiring the callback
- No new features
- No error reporting beyond the existing warning dialog
