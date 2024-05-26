import json

from locust import FastHttpUser, events, tag, task

from const.config import CONFIG
from utils.config_util import read_config

inference_data = []


class FlockLoadTestingKit(FastHttpUser):
    host = "https://api.deepinfra.com/v1"
    api_key = ""
    prompt = ""

    # api_key = ""
    # prompt = "test_prompt"

    # def __init__(self):
    #     config = read_config()
    #     self.api_key = config[CONFIG.API_KEY.value]
    #     self.prompt = config[CONFIG.PROMPT.value]

    def init_config(self):
        if not self.api_key or self.prompt:
            config = read_config()
            self.api_key = config[CONFIG.API_KEY.value]
            self.prompt = config[CONFIG.PROMPT.value]

    def print_response_data(self, response_data):
        print("Inference Status:")
        # inference_status = response_data.get("inference_status", {})
        # for key, value in inference_status.items():
        #     print(f"{key}: {value}")

        # print("\nResults:")
        # results = response_data.get("results", [])
        # for result in results:
        #     generated_text = result.get("generated_text", "")
        #     print(f"Generated Text:\n{generated_text}")

        print("\nNumber of Tokens:")
        print(f"Output: {response_data.get('num_tokens', 0)}")
        print(f"Input: {response_data.get('num_input_tokens', 0)}")

    def post_inference(self, model_tag):
        self.init_config()
        # print("User Prompt: ", self.prompt)
        response = self.client.post(
            url=f"/inference/{model_tag}",
            json={"input": self.prompt},
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response_data = json.loads(response.text)
        # self.print_response_data(response_data)
        inference_data.append(json.dumps(response_data["inference_status"]))

    @tag("microsoft/WizardLM-2-7B")
    @task
    def microsoft_WizardLM_2_7B(self):
        self.post_inference("microsoft/WizardLM-2-7B")

    @tag("meta-llama/Meta-Llama-3-8B-Instruct")
    @task
    def meta_llama_Meta_Llama_3_8B_Instruct(self):
        self.post_inference("meta-llama/Meta-Llama-3-8B-Instruct")

    @tag("mistralai/Mixtral-8x22B-Instruct-v0.1")
    @task
    def mistralai_Mixtral_8x22B_Instruct_v0_1(self):
        self.post_inference("mistralai/Mixtral-8x22B-Instruct-v0.1")

    @tag("openai/whisper-tiny")
    @task
    def openai_whisper_tiny(self):
        self.post_inference("openai/whisper-tiny")

    @tag("bigcode/starcoder2-15b")
    @task
    def bigcode_starcoder2_15b(self):
        self.post_inference("bigcode/starcoder2-15b")

    @tag("openchat/openchat_3.5")
    @task
    def openchat_openchat_3_5(self):
        self.post_inference("openchat/openchat_3.5")

    @tag("Gryphe/MythoMax-L2-13b")
    @task
    def gryphe_mythomax_L2_13b(self):
        self.post_inference("Gryphe/MythoMax-L2-13b")

    @tag("Phind/Phind-CodeLlama-34B-v2")
    @task
    def phind_phind_codellama_34B_v2(self):
        self.post_inference("Phind/Phind-CodeLlama-34B-v2")

    @tag("llava-hf/llava-1.5-7b-hf")
    @task
    def llava_hf_llava_1_5_7b_hf(self):
        self.post_inference("llava-hf/llava-1.5-7b-hf")

    @tag("google/gemma-1.1-7b-it")
    @task
    def google_gemma_1_1_7b_it(self):
        self.post_inference("google/gemma-1.1-7b-it")

    @tag("microsoft/WizardLM-2-8x22B")
    @task
    def microsoft_WizardLM_2_8x22B(self):
        self.post_inference("microsoft/WizardLM-2-8x22B")

    @tag("lizpreciatior/lzlv_70b_fp16_hf")
    @task
    def lizpreciatior_lzlv_70b_fp16_hf(self):
        self.post_inference("lizpreciatior/lzlv_70b_fp16_hf")

    def on_test_stop(environment, **kwargs):
        print("\n")
        print("Flocking Inference Data...")

        for index, inference_datum in enumerate(inference_data):
            inference_dict = json.loads(inference_datum)

            runtime_ms = inference_dict["runtime_ms"]
            cost = inference_dict["cost"]
            tokens_generated = inference_dict["tokens_generated"]
            tokens_input = inference_dict["tokens_input"]

            cost_per_sec = cost / runtime_ms
            tokens_per_sec = (tokens_generated + tokens_input) / runtime_ms
            output_to_input_factor = tokens_generated / tokens_input

            print(f"Inference Data for Prompt #{index + 1}...\n")

            print(f"Runtime (ms): {runtime_ms}")
            print(f"Cost: {cost} | Cost Per Sec: {cost_per_sec}")
            print(
                f"Output Tokens: {tokens_generated} | Input Tokens: {tokens_input} | Tokens Per Sec: {tokens_per_sec}"
            )
            print(f"Output to Input Token Ratio: {output_to_input_factor}")

            print("\n")

        print("Happy Flocking 🦅\n")

    events.test_stop.add_listener(on_test_stop)
