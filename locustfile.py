import json

from locust import FastHttpUser, events, tag, task

from const.config import CONFIG
from utils.config_util import read_config

inference_data = []


class FlockLoadTestingKit(FastHttpUser):
    host = "https://api.deepinfra.com/v1"
    api_key = ""
    prompt = ""
    model = ""

    def init_config(self):
        if self.api_key or self.prompt or self.model:
            return

        config = read_config()
        self.api_key = config[CONFIG.API_KEY.value]
        self.prompt = config[CONFIG.PROMPT.value]
        self.model = config[CONFIG.MODEL.value]

    @tag("llm")
    @task
    def call_llm(self):
        self.init_config()
        self.client.post(
            url=f"/inference/{self.model}",
            json={"input": self.prompt},
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        print("> Test loaded...")

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        print("\nInference Data for Prompts:")
        # print_inference_data(inference_data)
        print("inference_data", inference_data)
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
            f"> New request logged\n"
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


def print_inference_data(inference_data):
    for index, inference_datum in enumerate(inference_data):
        inference_dict = json.loads(inference_datum)

        runtime_ms = inference_dict["runtime_ms"]
        cost = inference_dict["cost"]
        tokens_generated = inference_dict["tokens_generated"]
        tokens_input = inference_dict["tokens_input"]

        cost_per_sec = cost / runtime_ms
        tokens_per_sec = (tokens_generated + tokens_input) / runtime_ms
        output_to_input_factor = tokens_generated / tokens_input

        print(f"Prompt #{index + 1}...")
        print(f"> Runtime (ms): {runtime_ms}")
        print(f"> Cost: {cost} | Cost Per Sec: {cost_per_sec}")
        print(f"> Output Tokens: {tokens_generated} | Input Tokens: {tokens_input}")
        print(f"> Tokens Per Sec: {tokens_per_sec}")
        print(f"> Output to Input Token Ratio: {output_to_input_factor}")
        print()
