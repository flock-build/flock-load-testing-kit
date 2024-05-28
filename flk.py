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


def run_locust(num_users, runtime):
    custom_locust_args = [
        "locust",
        "-f",
        "locustfile.py",
        "--headless",
        "--users",
        num_users,
        "--spawn-rate",
        "1",
        "--run-time",
        runtime,
        "--tags",
        "llm",
        "--csv",
        "temp/flk_fly",
        "--csv-full-history",
        "--html",
        "temp/flk_fly.html",
    ]
    subprocess.run(custom_locust_args, cwd=".")


def roost():
    subprocess.run(["locust"], cwd=".")


def fly():
    # get config
    config = get_config()

    # run locust
    run_locust(
        config[CONFIG.NUMBER_OF_USERS.value],
        config[CONFIG.RUNTIME.value],
    )

    # link to report
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
