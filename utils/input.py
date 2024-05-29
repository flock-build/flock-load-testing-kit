import os

from dotenv import load_dotenv

from const.config import CONFIG
from const.model_mapping import MODEL_MAPPING
from utils.config import save_config, update_config

load_dotenv()


def get_user_input() -> dict:
    """
    Prompt the user for configuration inputs and save them to a config file.

    Returns:
        dict: The configuration dictionary containing user inputs.
    """

    # init new config
    config = {}

    # request number of users
    num_users = __num_user_input()
    update_config(config, CONFIG.NUMBER_OF_USERS, num_users)

    # request runtime
    runtime = __runtime_input()
    update_config(config, CONFIG.RUNTIME, runtime)

    # request model
    model = __model_input()
    update_config(config, CONFIG.MODEL, MODEL_MAPPING[model])

    # request prompt
    prompt = __prompt_input()
    update_config(config, CONFIG.PROMPT, prompt)

    api_key = __api_key_input()
    update_config(config, CONFIG.API_KEY, api_key)

    # save config
    save_config(config)

    return config


def __prompt_input():
    val = input("\n🦅 Enter a prompt you want to analyze: ")
    if not val:
        val = os.environ.get("prompt")
    return val


def __api_key_input():
    val = input("\n🦅 Enter your DeepInfra API Key: ")
    if not val:
        val = os.environ.get("api_key")
    return val


def __model_input():
    print("\nWhich model would you like to test?\n")
    for key, value in MODEL_MAPPING.items():
        print(f"{key}) {value}")
    val = input(
        "\n🦅 Enter the number corresponding to the model you want to performance test: "
    )
    if not val:
        val = os.environ.get("model")
    return val


def __num_user_input():
    val = input("\n🦅 Enter the number of users you want to simulate: ")
    if not val:
        val = os.environ.get("num_user")
    return val


def __runtime_input():
    val = input("\n🦅 Enter how long you want to run your load test (Ex: 1h 30s): ")
    if not val:
        val = os.environ.get("runtime")
    return val
