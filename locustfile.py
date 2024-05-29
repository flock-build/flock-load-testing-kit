import json

from locust import FastHttpUser, events, tag, task
from locust.runners import MasterRunner

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
        response = self.client.post(
            url=f"/inference/{self.model}",
            json={"input": self.prompt},
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response_data = json.loads(response.text)
        inference_data.append(json.dumps(response_data["inference_status"]))

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        print("\n🦅 Flocking in progress...\n")

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        print("\n🦅 Flocking complete...\n")
        print_inference_data(inference_data)


def write_inference_data(inference_data):
    file_path = "temp/inference_data.json"
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

        print(f"Inference Data for Prompt #{index + 1}...")

        print(f"> Runtime (ms): {runtime_ms}")
        print(f"> Cost: {cost} | Cost Per Sec: {cost_per_sec}")
        print(
            f"> Output Tokens: {tokens_generated} | Input Tokens: {tokens_input} | Tokens Per Sec: {tokens_per_sec}"
        )
        print(f"> Output to Input Token Ratio: {output_to_input_factor}")

        print()
