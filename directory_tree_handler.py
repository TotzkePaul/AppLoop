import os
from ignore_scheme import IgnoreScheme

class DirectoryTreeHandler:
    def __init__(self, directory_path, ignore_scheme=None):
        self.directory_path = directory_path
        self.ignore_scheme = ignore_scheme if ignore_scheme is not None else IgnoreScheme(ignored_files = [".DS_Store", "package-lock.json", ""])


    def get_tree_dict(self, path=None):
        if path is None:
            path = self.directory_path
        tree = {}
        for root, dirs, files in os.walk(path):
            if self.ignore_scheme.should_ignore_dir(root):
                continue
            filtered_files = [f for f in files if not self.ignore_scheme.should_ignore_file(f)]
            filtered_dirs = [d for d in dirs if not self.ignore_scheme.should_ignore_dir(os.path.join(root, d))]
            tree[root] = {'files': filtered_files, 'dirs': filtered_dirs}
        return tree

    def get_tree_string(self):
        tree_dict = self.get_tree_dict()
        tree_str = ""

        def build_tree_string(path, level=0):
            nonlocal tree_str
            indent = ' ' * 2 * level
            tree_str += '{}{}/\n'.format(indent, os.path.basename(path))
            subindent = ' ' * 2 * (level + 1)

            for file in tree_dict[path]['files']:
                tree_str += '{}-{}\n'.format(subindent, file)

            for subdir in tree_dict[path]['dirs']:
                subdir_path = os.path.join(path, subdir)
                if subdir_path in tree_dict:
                    build_tree_string(subdir_path, level + 1)

        build_tree_string(self.directory_path)
        return tree_str.strip()


    @staticmethod
    def compare_trees(original_tree_str, target_tree_str):
        original_files = set(original_tree_str.splitlines())
        target_files = set(target_tree_str.splitlines())
        missing_files = list(original_files - target_files)
        return missing_files

    def concatenate_file_contents(self):
        combined_content = ""
        for root, _, files in os.walk(self.directory_path):
            for file in files:
                if file not in self.ignored_files:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        combined_content += f"\n{file}:\n"
                        combined_content += f.read()
        return combined_content

# Example usage
# ignored_files = ['.DS_Store']
# dir_handler = DirectoryTreeHandler('/path/to/directory', ignored_files)
# tree_dict = dir_handler.get_tree_dict()
# tree_str = dir_handler.get_tree_string()
# missing_files = DirectoryTreeHandler.compare_trees(tree_str1, tree_str2)
# combined_content = dir_handler.concatenate_file_contents()
