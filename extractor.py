import csv
import fnmatch
import os
import pypdf
import re


class MD5Extractor:
    """Extract MD5-shaped values from PDF files and write CSV-style output."""

    MD5_PATTERN = r'[a-fA-F0-9]{32}'

    def __init__(self, directory, save_path):
        """Create an extractor for a PDF directory and output file path."""
        self.directory = directory
        self.save_path = save_path
        self.results = {}
        self.errors = []

    def dir_exists(self):
        """Return True when the configured input directory exists."""
        return os.path.isdir(self.directory)

    def read_dir(self):
        """Return a sorted list of PDF paths found below the input directory."""
        paths = []
        for root, _, files in os.walk(self.directory):
            for filename in fnmatch.filter(files, '*.pdf'):
                paths.append(os.path.join(root, filename))
        return sorted(paths)

    def get_pdf_content(self, path):
        """Extract and return text content from every page in a PDF file."""
        content = ""
        with open(path, "rb") as fh:
            pdf = pypdf.PdfReader(fh)
            for page in pdf.pages:
                content += (page.extract_text() or "") + "\n"
        return content

    def extract(self, progress_callback=None, status_callback=None, result_callback=None):
        """Scan PDFs, emit optional callbacks, write output, and return results.

        Args:
            progress_callback: Optional callable receiving an integer percentage.
            status_callback: Optional callable receiving skipped-file messages.
            result_callback: Optional callable receiving each ``pdf_path, md5`` pair.

        Returns:
            A dictionary mapping PDF paths to sets of unique MD5-shaped values.
        """
        self.results = {}
        self.errors = []
        pdfs = self.read_dir()
        total = len(pdfs)

        for count, pdf in enumerate(pdfs, start=1):
            try:
                content = self.get_pdf_content(pdf)
                self.results[pdf] = set(re.findall(self.MD5_PATTERN, content))
            except Exception as error:
                self.errors.append((pdf, str(error)))
                if status_callback is not None:
                    status_callback("Skipped %s: %s" % (pdf, error))
            else:
                if result_callback is not None:
                    for md5 in sorted(self.results[pdf]):
                        result_callback(pdf, md5)

            if progress_callback is not None and total > 0:
                progress_callback(int(count * 100 / total))

        self.write_data()
        return self.results

    def write_data(self):
        """Append extracted PDF/hash pairs to the configured output file."""
        with open(self.save_path, mode='a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Absolute_Path', 'MD5_Hash_Values'])
            for pdf, md5s in sorted(self.results.items()):
                for md5 in sorted(md5s):
                    writer.writerow([pdf, md5])
