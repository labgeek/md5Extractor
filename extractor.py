import fnmatch
import os


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
