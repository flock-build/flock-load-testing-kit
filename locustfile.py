from locust import FastHttpUser, task, events, tag
import time
import json
from flk import USER_PROMPT

inference_data = []

class FlockLoadTestingKit(FastHttpUser):
    host = "https://api.deepinfra.com/v1"

    def post_inference(self, model_tag):
        print("User Prompt:\n")
        print(USER_PROMPT)
        response = self.client.post(
            url=f"/inference/{model_tag}", 
            json={"input": USER_PROMPT},
            headers={"Authorization": "Bearer Eit9lqbVKtSLejQ25UCmg9gOs761aWNs"}
        )
        response_data = json.loads(response.text)
        print(response_data)
        inference_data.append(json.dumps(response_data['inference_status']))

    @tag('microsoft/WizardLM-2-7B')
    @task
    def microsoft_WizardLM_2_7B(self):
        self.post_inference('microsoft/WizardLM-2-7B')

    @tag('meta-llama/Meta-Llama-3-8B-Instruct')
    @task
    def meta_llama_Meta_Llama_3_8B_Instruct(self):
        self.post_inference('meta-llama/Meta-Llama-3-8B-Instruct')

    @tag('mistralai/Mixtral-8x22B-Instruct-v0.1')
    @task
    def mistralai_Mixtral_8x22B_Instruct_v0_1(self):
        self.post_inference('mistralai/Mixtral-8x22B-Instruct-v0.1')

    @tag('openai/whisper-tiny')
    @task
    def openai_whisper_tiny(self):
        self.post_inference('openai/whisper-tiny')

    @tag('bigcode/starcoder2-15b')
    @task
    def bigcode_starcoder2_15b(self):
        self.post_inference('bigcode/starcoder2-15b')

    @tag('openchat/openchat_3.5')
    @task
    def openchat_openchat_3_5(self):
        self.post_inference('openchat/openchat_3.5')

    @tag('Gryphe/MythoMax-L2-13b')
    @task
    def gryphe_mythomax_L2_13b(self):
        self.post_inference('Gryphe/MythoMax-L2-13b')
    
    @tag('Phind/Phind-CodeLlama-34B-v2')
    @task
    def phind_phind_codellama_34B_v2(self):
        self.post_inference('Phind/Phind-CodeLlama-34B-v2')
    
    @tag('llava-hf/llava-1.5-7b-hf')
    @task
    def llava_hf_llava_1_5_7b_hf(self):
        self.post_inference('llava-hf/llava-1.5-7b-hf')

    @tag('google/gemma-1.1-7b-it')
    @task
    def google_gemma_1_1_7b_it(self):
        self.post_inference('google/gemma-1.1-7b-it')

    @tag('microsoft/WizardLM-2-8x22B')
    @task
    def microsoft_WizardLM_2_8x22B(self):
        self.post_inference('microsoft/WizardLM-2-8x22B')
    
    @tag('lizpreciatior/lzlv_70b_fp16_hf')
    @task
    def lizpreciatior_lzlv_70b_fp16_hf(self):
        self.post_inference('lizpreciatior/lzlv_70b_fp16_hf')

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
            print(f"Output Tokens: {tokens_generated} | Input Tokens: {tokens_input} | Tokens Per Sec: {tokens_per_sec}")
            print(f"Output to Input Token Ratio: {output_to_input_factor}")

            print("\n")

        print("Happy Flocking 🦅\n") 
        
    events.test_stop.add_listener(on_test_stop)
