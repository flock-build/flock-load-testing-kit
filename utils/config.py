import json
import os

from const.config import CONFIG

DIRECTORY = "temp"
CONFIG_FILE_NAME = "config.json"


# Populate config
def update_config(config: dict, config_option: CONFIG, value: str):
    """
    Update a configuration option in the given config dictionary.

    Args:
        config (dict): The configuration dictionary.
        config_option (CONFIG): The configuration option to update.
        value (str): The new value for the configuration option.
    """
    config[config_option.value] = value


# Save config.json to temp
def save_config(config: dict):
    """
    Save the configuration dictionary to config.json file in the temp directory.

    Args:
        config (dict): The configuration dictionary.
    """
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    file_path = os.path.join(DIRECTORY, CONFIG_FILE_NAME)
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w") as file:
        json.dump(config, file)


def read_config() -> dict:
    """
    Read the configuration from the config.json file in the temp directory.

    Returns:
        dict: The configuration dictionary read from the file.
    """
    file_path = os.path.join(DIRECTORY, CONFIG_FILE_NAME)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        # If the file doesn't exist, return an empty dictionary
        raise FileNotFoundError(f"Configuration file '{file_path}' not found.")
