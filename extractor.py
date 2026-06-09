import csv
import fnmatch
import os
import pypdf
import re


class MD5Extractor:
    MD5_PATTERN = r'[a-fA-F0-9]{32}'

    def __init__(self, directory, save_path):
        self.directory = directory
        self.save_path = save_path
        self.results = {}

    def dir_exists(self):
        return os.path.isdir(self.directory)

    def read_dir(self):
        paths = []
        for root, _, files in os.walk(self.directory):
            for filename in fnmatch.filter(files, '*.pdf'):
                paths.append(os.path.join(root, filename))
        return paths

    def get_pdf_content(self, path):
        content = ""
        with open(path, "rb") as fh:
            pdf = pypdf.PdfReader(fh)
            for page in pdf.pages:
                content += (page.extract_text() or "") + "\n"
        return content

    def extract(self, progress_callback=None):
        pdfs = self.read_dir()
        total = len(pdfs)

        for count, pdf in enumerate(pdfs, start=1):
            try:
                content = self.get_pdf_content(pdf)
                self.results[pdf] = set(re.findall(self.MD5_PATTERN, content))
            except Exception:
                continue

            if progress_callback is not None and total > 0:
                progress_callback(int(count * 100 / total))

        self.write_data()
        return self.results

    def write_data(self):
        with open(self.save_path, mode='a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(['Absolute_Path', 'MD5_Hash_Values'])
            for pdf, md5s in self.results.items():
                for md5 in md5s:
                    writer.writerow([pdf, md5])
