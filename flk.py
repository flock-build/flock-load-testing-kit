import os
import subprocess
import sys
import urllib.parse

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
        "--csv",
        "temp/flk_fly",
        "--csv-full-history",
        "--html",
        "temp/fly_fly.html",
    ]
    subprocess.run(custom_locust_args, cwd=".")


def roost():
    subprocess.run(["locust"], cwd=".")


def fly():
    config = get_config()
    run_locust(
        config[CONFIG.NUMBER_OF_USERS.value],
        config[CONFIG.RUNTIME.value],
        config[CONFIG.MODEL.value],
    )
    file_path = "temp/flk_fly.html"
    absolute_path = os.path.abspath(file_path)
    print(
        "Link to Results: ",
        urllib.parse.urljoin("file:", urllib.parse.quote(absolute_path)),
    )


def main():
    if sys.argv[1] == "fly" and sys.argv[2] == "llm":
        fly()
    elif sys.argv[1] == "roost":
        roost()
    else:
        print("Usage: flk [fly (cli)|roost (web)]")


if __name__ == "__main__":
    main()
