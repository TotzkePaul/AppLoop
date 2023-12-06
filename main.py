from directory_tree_handler import DirectoryTreeHandler

def main():
    # Set the directory paths for testing
    original_dir_path = './dist'
    target_dir_path = './target'

    # Create DirectoryTreeHandler instances
    original_dir_handler = DirectoryTreeHandler(original_dir_path)
    target_dir_handler = DirectoryTreeHandler(target_dir_path)

    # 1. Get tree as dict
    original_tree_dict = original_dir_handler.get_tree_dict()
    print("Original Directory Tree as Dict:")
    print(original_tree_dict)

    # 2. Get tree as string
    original_tree_str = original_dir_handler.get_tree_string()
    print("\nOriginal Directory Tree as String:")
    print(original_tree_str)

    # For target directory
    target_tree_str = target_dir_handler.get_tree_string()
    print("\nTarget Directory Tree as String:")
    print(target_tree_str)

    # 3. Compare two tree-strings and get missing file paths
    missing_files = DirectoryTreeHandler.compare_trees(original_tree_str, target_tree_str)
    print("\nMissing Files:")
    print(missing_files)

    # 4. Concatenate file contents
    concatenated_content = original_dir_handler.concatenate_file_contents()
    print("\nConcatenated File Contents:")
    print(concatenated_content)

if __name__ == "__main__":
    main()
