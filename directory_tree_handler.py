import os

class DirectoryTreeHandler:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def get_tree_dict(self, path=None):
        if path is None:
            path = self.directory_path
        tree = {}
        for root, dirs, files in os.walk(path):
            tree[root] = {'files': files, 'dirs': dirs}
        return tree

    def get_tree_string(self, path=None, prefix=''):
        if path is None:
            path = self.directory_path
        tree_str = ""
        for root, dirs, files in os.walk(path):
            level = root.replace(path, '').count(os.sep)
            indent = ' ' * 2 * level
            tree_str += '{}{}/\n'.format(indent, os.path.basename(root))
            subindent = ' ' * 2 * (level + 1)
            for f in files:
                tree_str += '{}-{}\n'.format(subindent, f)
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
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    combined_content += f"\n{file}:\n"
                    combined_content += f.read()
        return combined_content

# Example usage
# dir_handler = DirectoryTreeHandler('/path/to/directory')
# tree_dict = dir_handler.get_tree_dict()
# tree_str = dir_handler.get_tree_string()
# missing_files = DirectoryTreeHandler.compare_trees(tree_str1, tree_str2)
# combined_content = dir_handler.concatenate_file_contents()
