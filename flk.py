import subprocess
import sys

from const.config import CONFIG
from utils.config_util import save_config
from utils.input_util import get_user_input


def get_config() -> dict:
    config = get_user_input()
    save_config(config)
    return config


def run_locust(num_users, runtime, model):
    custom_locust_args = [
        "locust",
        "-f",
        "locustfile.py",
        "--headless",
        "-u",
        num_users,
        "--run-time",
        runtime,
        "--tags",
        model,
    ]
    subprocess.run(custom_locust_args, cwd=".")


def run_locust_ui():
    subprocess.run(["locust"], cwd=".")


def main():
    if sys.argv[1] == "fly" and sys.argv[2] == "llm":
        config = get_config()
        run_locust(
            config[CONFIG.NUMBER_OF_USERS.value], config[CONFIG.RUNTIME.value], config[CONFIG.MODEL.value]
        )
    elif sys.argv[1] == "roost":
        run_locust_ui()
    else:
        print("Usage: flk [fly (cli)|roost (web)]")


if __name__ == "__main__":
    main()
