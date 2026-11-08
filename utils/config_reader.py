
# Loads the test configuration from the YAML file and returns it as a dictionary.

import yaml
from pathlib import Path


class ConfigReader:

    @staticmethod
    def load_test_data():

        # Builds the path to the YAML configuration file
        file_path = (
            Path(__file__).parent.parent
            / "data"
            / "test_data.yaml"
        )

        # Opens the YAML file and loads its content as a Python dictionary
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
