import json
import os
import subprocess
import urllib.parse
import uuid

from const.config import CONFIG
from utils.config import save_config
from utils.data_processing import clean_up_locust_data
from utils.input import get_user_input
from utils.mongo import save_to_mongo


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

    # link to inference data
    __save_inference_data(config[CONFIG.SESSION_ID.value])

    # link to report
    __generate_locust_report_link()

    print(f"Session ID: {config[CONFIG.SESSION_ID.value]}")


def __generate_locust_report_link():
    file_path = "temp/flk_fly.html"
    absolute_path = os.path.abspath(file_path)
    print(
        "Link to Test Report: ",
        urllib.parse.urljoin("file:", urllib.parse.quote(absolute_path)),
    )


def __save_inference_data(guid: str):
    file_path = "temp/flk_fly_inference_data.json"

    # save inference data to mongo
    with open(file_path, "r") as file:
        data = json.load(file)

    processed_data = clean_up_locust_data(data, guid)

    save_to_mongo(processed_data)

    # save inference data to temp directory
    absolute_path = os.path.abspath(file_path)
    print(
        "Link to Inference Data: ",
        urllib.parse.urljoin("file:", urllib.parse.quote(absolute_path)),
    )


def __get_config() -> dict:
    config = get_user_input()
    config[CONFIG.SESSION_ID.value] = str(uuid.uuid4())
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
