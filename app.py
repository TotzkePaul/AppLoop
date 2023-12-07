import json
import os
import sys
from pathlib import Path
from jsonschema import validate  # For JSON schema validation
import requests  # For making API requests, e.g., to OpenAI
from dotenv import load_dotenv  # To load environment variables
import logging  # For logging
import openai 
from jsonschema.exceptions import ValidationError
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY")
)

def load_config(path):
    with open(path, "r") as f:
        # Reading from file
        data = json.loads(f.read())
    return data

CONFIG_SCHEMA = load_config('type.schema.json')

def main_loop(config_file_path, directory_path):
    # Load and validate configuration
    #config = load_config(config_file_path)
    #if not validate_config(config, CONFIG_SCHEMA):
    #    raise ValueError("Invalid configuration")

    # Construct source and target structures
    source_tree = scan_directory(directory_path)
    source_string = convert_directory_structure_to_string(source_tree)
    print(source_string)
    target_tree = create_target_structure(source_string)

    # Perform comparison and take action
    differences, common_elements = compare_structures(source_tree, target_tree)
    generate_files(differences, config)
    update_files(common_elements, config)

    # Log activities
    # activity_log = gather_activities()  # Implement gather_activities to summarize actions
    # log_activities(activity_log)


def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON format in file: {file_path}")
        return None

def validate_config(config, schema):
    try:
        validate(instance=config, schema=schema)
        return True
    except ValidationError as ve:
        print("JSON Validation Error:", ve.message)
        return False



def scan_directory(directory):
    directory_structure = {}

    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        relative_path = root_path.relative_to(directory)
        directory_structure[str(relative_path)] = files
    
    return directory_structure

def convert_directory_structure_to_string(directory_structure, indent=0):
    tree = ""
    for folder, files in directory_structure.items():
        tree += "  " * indent + folder + "\n"
        for file in files:
            tree += "  " * (indent + 1) + file + "\n"
    return tree


def create_target_structure(source_string):

    result = integrate_openai(messages);
    target_structure = {}

    # Assuming config contains a structure key with desired directories and files
    for folder, files in config.get('structure', {}).items():
        target_structure[folder] = files
    
    return target_structure


def compare_structures(source, target):
    differences = {
        'create': [],  # List of paths to create
        'update': []   # List of paths to update
    }

    # Check what's in target but not in source (to be created)
    for path, files in target.items():
        if path not in source:
            differences['create'].append((path, files))
        else:
            # Check for files that are in target but not in source
            missing_files = [file for file in files if file not in source[path]]
            if missing_files:
                differences['create'].append((path, missing_files))

    # Optionally, identify files that need updating
    # ...

    return differences



def generate_files(differences, config):
    for path, files in differences['create']:
        # Create directory if it doesn't exist
        os.makedirs(path, exist_ok=True)

        for file in files:
            file_path = os.path.join(path, file)
            with open(file_path, 'w') as f:
                # Optionally, write starter content to files
                starter_content = config.get('fileTemplates', {}).get(file, '')
                f.write(starter_content)


def update_files(common_elements, config):
    for path, files in common_elements.items():
        for file in files:
            file_path = os.path.join(path, file)
            # Define your update logic here
            # Example: appending data, modifying content, etc.
            with open(file_path, 'a') as f:  # 'a' for append, change as needed
                update_content = config.get('updateContent', {}).get(file, '')
                f.write(update_content)

import requests



def integrate_openai(input_text):
    messages = []
    for text in input_text:
        messages.append({
            "role": "user",
            "content": text,
        })

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-4-1106-preview",
    )

    file_contents = chat_completion.choices[0].message.content

    return file_contents

def log_activities(activity_log):
    logging.basicConfig(filename='app_activities.log', level=logging.INFO)
    for log in activity_log:
        logging.info(log)

    return None


def log_activities(activity_log):
    logging.basicConfig(filename='app_activities.log', level=logging.INFO)
    for log in activity_log:
        logging.info(log)


def main():
    config = load_config('type.schema.json')
    dir_path = './dist'
    main_loop(config, dir_path)

if __name__ == "__main__":
    main() 