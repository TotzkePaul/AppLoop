import unittest
import os
import json
from jsonschema import validate 
from jsonschema.exceptions import ValidationError


def validate_config(config, schema):
    try:
        validate(instance=config, schema=schema)
        return True
    except ValidationError as ve:
        print("JSON Validation Error:", ve.message)
        return False
def load_config(path):
    with open(path, "r") as f:
        # Reading from file
        data = json.loads(f.read())
    return data

class TestConfigManager(unittest.TestCase):


    def test_load_config_valid(self):
        # Test loading a valid config file
        config_file_path = os.path.join(os.path.dirname(__file__), "expect.schema.json")
        expected_config = load_config(config_file_path)

        config_file_path = os.path.join(os.path.dirname(__file__), "../type.schema.json")
        # Call the load_config function
        actual_config = load_config(config_file_path)

        #print("Expected Config:", expected_config)
        #print("Actual Config:", actual_config)

        validate_config(actual_config, expected_config)
        

# This allows running the tests from the command line
if __name__ == '__main__':
    unittest.main()
