import fnmatch
import os

class IgnoreScheme:
    def __init__(self, ignored_files=None, ignored_patterns=None, ignored_dirs=None):
        self.ignored_files = ignored_files if ignored_files is not None else []
        self.ignored_patterns = ignored_patterns if ignored_patterns is not None else []
        self.ignored_dirs = ignored_dirs if ignored_dirs is not None else []

    def should_ignore_file(self, file_name):
        if file_name in self.ignored_files:
            return True
        for pattern in self.ignored_patterns:
            if fnmatch.fnmatch(file_name, pattern):
                return True
        return False

    def should_ignore_dir(self, dir_path):
        for dir_pattern in self.ignored_dirs:
            if fnmatch.fnmatch(dir_path, dir_pattern):
                return True
        return False
