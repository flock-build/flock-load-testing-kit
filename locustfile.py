import json

from locust import FastHttpUser, events, tag, task

from const.config import CONFIG
from utils.config import read_config

inference_data = []


class FlockLoadTestingKit(FastHttpUser):
    host = "https://api.deepinfra.com/v1"
    config = {}

    def init_config(self):
        if self.config:
            return

        self.config = read_config()

    @tag("llm")
    @task
    def call_llm(self):
        self.init_config()
        self.client.post(
            url=f"/inference/{self.config[CONFIG.MODEL.value]}",
            json={"input": self.config[CONFIG.PROMPT.value]},
            headers={"Authorization": f"Bearer {self.config[CONFIG.API_KEY.value]}"},
        )

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        print("> Test loaded...")

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        write_inference_data(inference_data)

    @events.request.add_listener
    def on_request_complete(
        request_type,
        name,
        response_time,
        response_length,
        response,
        context,
        exception,
        start_time,
        url,
        **kwargs,
    ):
        data = {
            "url": url,
            "name": name,
            "request_type": request_type,
            "start_time": start_time,
            "response_time": response_time,
            "response_length": response_length,
            "response": response.json(),
            "context": context,
        }

        inference_data.append(data)
        print(
            f"\n> New request logged\n"
            f"  - Request Type   : {request_type}\n"
            # f"  - Name           : {name}\n"
            f"  - URL            : {url}\n"
            f"  - Start Time     : {start_time}\n"
            f"  - Response Time  : {response_time} ms\n"
            f"  - Response Length: {response_length} bytes\n"
            # f"  - Exception      : {exception}\n"
            # f"  - Context        : {context}\n"
            # f"  - Additional Info: {kwargs}\n"
            # f"  - Response       : {response.json()}\n"
        )

    @events.spawning_complete.add_listener
    def on_spawning_complete(user_count, **kwargs):
        print(f"> All users ({user_count}) spawned...")

    @events.cpu_warning.add_listener
    def cpu_warning():
        print("> CPU usage >90%")


def write_inference_data(inference_data):
    file_path = "temp/flk_fly_inference_data.json"
    with open(file_path, "w") as json_file:
        json.dump(inference_data, json_file)
