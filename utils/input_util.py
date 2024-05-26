from const.config import CONFIG
from const.model_mapping import MODEL_MAPPING
from utils.config_util import save_config, update_config


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

    print("\n")
    print("Initiating load test...")
    print("\n")

    return config


def __prompt_input():
    print("\n")
    print("🦅 What prompt do you want to run? 🦅")
    prompt = input("Enter a prompt you want to analyze: ")
    return prompt


def __api_key_input():
    print("\n")
    print("🦅 What is your deepinfra API key? 🦅")
    prompt = input("Enter API Key: ")
    return prompt


def __model_input():
    print("\n")
    print("🦅 Which model would you like to Flock? 🦅")
    for key, value in MODEL_MAPPING.items():
        print(f"{key}) {value}")
    model = input(
        "Enter the number corresponding to the model you want to performance test: "
    )

    return model


def __num_user_input():
    print("\n")
    print("🦅 How many users do you want to simulate? 🦅")
    num_users = input("Enter the number of users you want to simulate: ")
    return num_users


def __runtime_input():
    print("\n")
    print("🦅 How long do you want to run your load test? 🦅")
    runtime = input("Enter how long you want to run your load test (Ex: 1h 30s): ")
    return runtime
