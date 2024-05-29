import os
import subprocess
import urllib.parse

from const.config import CONFIG
from utils.config import save_config
from utils.input import get_user_input


def fly():
    """
    Start FLK Load testing.

    Retrieves user input, saves config and runs locust.

    Once completes, saves test data into temp directory
    """

    # get config
    config = __get_config()

    # run locust
    print("\n🦅 Flocking in progress...\n")
    __run_locust(
        config[CONFIG.NUMBER_OF_USERS.value],
        config[CONFIG.RUNTIME.value],
    )
    print("\n🦅 Flocking complete...\n")

    # link to report
    __generate_locust_report_link()

    # link to inference data
    __save_inference_data()


def __generate_locust_report_link():
    file_path = "temp/flk_fly.html"
    absolute_path = os.path.abspath(file_path)
    print(
        "Link to Test Report: ",
        urllib.parse.urljoin("file:", urllib.parse.quote(absolute_path)),
    )


def __save_inference_data():
    file_path = "temp/flk_fly_inference_data.json"
    absolute_path = os.path.abspath(file_path)
    print(
        "Link to Inference Data: ",
        urllib.parse.urljoin("file:", urllib.parse.quote(absolute_path)),
    )


def __get_config() -> dict:
    config = get_user_input()
    save_config(config)
    return config


def __run_locust(num_users, runtime):
    custom_locust_args = [
        "locust",
        "-f",
        "locustfile.py",
        "--headless",
        "--users",
        num_users,
        # "--spawn-rate",
        # "1",
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
