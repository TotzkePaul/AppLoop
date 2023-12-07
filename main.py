from directory_tree_handler import DirectoryTreeHandler
from ignore_scheme import IgnoreScheme
from openai import OpenAI
import os

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY")
)

def integrate_openai(input_text):
    messages = []

    messages.append({
            "role": "system",
            "content": "You look at a tree of files in an angular project. \
                You only reply with another tree of files that would be required \
                    to fufill the user's request. No additional comments, only a tree \
                        reprentation of the files. Use a flat list where the Folder is labeled as its full relative path.\
                            Files should be this format: \"{- filename-no-path}\
                                Not just the changes, but the entire tree.",
        })
    for text in input_text:
        messages.append({
            "role": "user",
            "content": text,
        })

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-1106-preview",
    )

    file_contents = chat_completion.choices[0].message.content[3:-3]

    return file_contents

def main():
    # Set the directory paths for testing
    original_dir_path = './dist'
    target_dir_path = './target'

 

    ignored_files = [".DS_Store", "package-lock.json", "favicon.ico"]
    ignored_patterns = ['*.jpeg', '*.jpg', '*.png']
    ignored_dirs = ['.git/*']

    ignore_scheme = IgnoreScheme(ignored_files, ignored_patterns, ignored_dirs)


    # Create DirectoryTreeHandler instances
    original_dir_handler = DirectoryTreeHandler(original_dir_path, None, ignore_scheme)
    target_dir_handler = DirectoryTreeHandler(target_dir_path, None, ignore_scheme)

    # 1. Get tree as dict
    original_tree_dict = original_dir_handler.get_tree_dict()
    print("Original Directory Tree as Dict:")
    print(original_tree_dict)

    # 2. Get tree as string
    original_tree_str = original_dir_handler.get_tree_string()
    print("\nOriginal Directory Tree as String:")
    print(original_tree_str)

    with open(target_dir_path + "/tree.txt", "w") as file:
        file.write(original_tree_str)

    intro = "I want to add a clock compentent to an angular project.\n"
    intro += "Below is a tree of the files in the project.\n"
    instruct = "Modify the tree with the file additions for the clock files.\n"
    instruct += "Reply with the tree of an angular project that would have the tooltip component. "
    instruct += "No additional comments, only a tree reprentation of the files. Not just the deltas, but the entire tree.\n"
    instruct += "for example:\n\n./SplashPage/app/src/app\n- tooltip.component.html\n- tooltip.component.scss\n- tooltip.component.spec.ts\n- app.component.ts"
    prompt = f"{intro}\n\n{original_tree_str}:\n\n{instruct}"

    ai_tree_str = integrate_openai(prompt)
    copy = DirectoryTreeHandler(tree_str = ai_tree_str)

    copy_str = copy.get_tree_string()


    

    with open(target_dir_path + "/tree.copy.txt", "w") as file:
        file.write(copy_str)

    # For target directory
    target_tree_str = target_dir_handler.get_tree_string()
    print("\nTarget Directory Tree as String:")
    print(target_tree_str)

    

    # 3. Compare two tree-strings and get missing file paths
    missing_files = copy.compare_trees(original_dir_handler)
    print("\nMissing Files:")
    print(missing_files)

    # 4. Concatenate file contents
    concatenated_content = original_dir_handler.concatenate_file_contents()
    print("\nConcatenated File Contents:")
    # print(concatenated_content)

    # Save concatenated_content to "files.txt" in target directory
    with open(target_dir_path + "/files.txt", "w") as file:
        file.write(concatenated_content)

if __name__ == "__main__":
    main()
    

