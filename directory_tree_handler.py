import os
from ignore_scheme import IgnoreScheme

class DirectoryTreeHandler:
    def __init__(self, directory_path = None, tree_str = None, ignore_scheme=None):
        self.ignore_scheme = ignore_scheme if ignore_scheme is not None else IgnoreScheme(ignored_files = [".DS_Store", "package-lock.json", ""])
        
        if directory_path:
            self.directory_path = directory_path
            self.tree_dict = self.get_tree_dict()
        else:
            self.directory_path = '.'
            self.tree_dict = self.string_to_tree_dict(tree_str)

    def string_to_tree_dict(self, tree_string):
        lines = tree_string.split('\n')
        tree_dict = {}
        current_path = []

        for line in lines:
            stripped_line = line.strip()
            if line == '':
                continue
            if stripped_line.startswith("-"):  # It's a file
                file_name = stripped_line[1:].strip()
                dir_path = '/'.join(current_path)
                if dir_path not in tree_dict:
                    tree_dict[dir_path] = {'files': []}
                tree_dict[dir_path]['files'].append(file_name)
            else:  # It's a directory
                depth = (len(line) - len(stripped_line)) // 2
                dir_name = stripped_line
                current_path = current_path[:depth]
                current_path.append(dir_name)
                dir_path = '/'.join(current_path)
                if dir_path not in tree_dict:
                    tree_dict[dir_path] = {'files': []}

        return tree_dict
    
    def get_tree_dict(self, path=None):
        if path is None:
            path = self.directory_path
        tree = {}
        for root, dirs, files in os.walk(path):
            if self.ignore_scheme.should_ignore_dir(root):
                continue
            filtered_files = [f for f in files if not self.ignore_scheme.should_ignore_file(f)]
            # filtered_dirs = [d for d in dirs if not self.ignore_scheme.should_ignore_dir(os.path.join(root, d))]
            idx = root.replace(path, ".", 1)
            tree[idx] = {'files': filtered_files}
        return tree


    def get_tree_string(self):
        tree_dict = self.tree_dict
        tree_str = ""

        for path in sorted(tree_dict.keys()):
            depth = path.count('/')
            indent = ''
            dir_name = path
            if depth == 0:  # Root directory
                tree_str += f"{dir_name}\n"
            else:
                tree_str += f"{indent}{dir_name}\n"

            for file in sorted(tree_dict[path]['files']):
                tree_str += f"{indent}- {file}\n"

        return tree_str.strip()


    def compare_trees(self, target):
        target_tree = target.tree_dict
        original_tree = self.tree_dict
        missing_files_tree = {}

        for path, content in original_tree.items():
            if path not in target_tree:
                missing_files_tree[path] = content
            else:
                missing_files = [file for file in content['files'] if file not in target_tree[path]['files']]
                if missing_files:
                    missing_files_tree[path] = {'files': missing_files}

        return missing_files_tree

    def concatenate_file_contents(self):
        tree_dict = self.tree_dict
        combined_content = ""

        def concatenate_from_path(path):
            nonlocal combined_content
            for file in tree_dict[path]['files']:
                file_path = os.path.join(path, file)
                with open(file_path, 'r') as f:
                    combined_content += f"\n{file}:\n"
                    combined_content += f.read()

            for subdir in tree_dict[path]['dirs']:
                subdir_path = os.path.join(path, subdir)
                if subdir_path in tree_dict:
                    concatenate_from_path(subdir_path)

        concatenate_from_path(self.directory_path)
        return combined_content
 

# Example usage
# ignored_files = ['.DS_Store']
# dir_handler = DirectoryTreeHandler('/path/to/directory', ignored_files)
# tree_dict = dir_handler.get_tree_dict()
# tree_str = dir_handler.get_tree_string()
# missing_files = DirectoryTreeHandler.compare_trees(tree_str1, tree_str2)
# combined_content = dir_handler.concatenate_file_contents()
