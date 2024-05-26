import subprocess
import sys

from consts import model_mapping

USER_PROMPT = ""

def set_user_prompt(prompt):
    USER_PROMPT = prompt

def user_input():
    print("\n")
    print("🦅 What prompt do you want to run? 🦅")
    prompt = input("Enter a prompt you want to analyze: ")
    set_user_prompt(prompt)
    print("\n")

    print("🦅 How many users do you want to simulate? 🦅")
    num_users = input("Enter the number of users you want to simulate: ")
    print('\n')

    print("🦅 How long do you want to run your load test? 🦅")
    runtime = input("Enter how long you want to run your load test (Ex: 1h 30s): ")
    print('\n')

    print("🦅 Which model would you like to Flock? 🦅")
    print("\n")
    print("Available Models...\n")
    print("1) microsoft/WizardLM-2-7B - Fast and achieves comparable performance with existing 10x larger open-source leading models")
    print("2) meta-llama/Meta-Llama-3-8B-Instruct - A collection of pretrained and instruction tuned generative text models in 8 and 70B sizes")
    print("3) mistralai/Mixtral-8x22B-Instruct-v0.1 - Latest and largest mixture of experts large language model (LLM) from Mistral AI")
    print("\n")
    print("Alternatives:\n")
    print("4) bigcode/starcoder2-15b")
    print("5) openchat/openchat_3.5")
    print("6) Gryphe/MythoMax-L2-13b")
    print("7) Phind/Phind-CodeLlama-34B-v2")
    print("8) llava-hf/llava-1.5-7b-hf")
    print("9) google/gemma-1.1-7b-it")
    print("10) microsoft/WizardLM-2-7B")
    print("11) lizpreciatior/lzlv_70b_fp16_hf")
    print("\n")
    model_choice = input("Enter the number corresponding to the model you want to performance test: ")

    return prompt, num_users, runtime, model_choice


def locust_pipeline(prompt, num_users, runtime, model_choice):
    model_id_name_conversion = model_mapping[model_choice]
    custom_locust_args = ["locust", "-f", "locustfile.py", "--headless", "-u", num_users, "--run-time", runtime, "--tags", model_id_name_conversion]
    subprocess.run(custom_locust_args, cwd=".")


def main():
    if sys.argv[1] == "fly" and sys.argv[2] == "llm":
        prompt, num_users, runtime, model_choice = user_input()
        locust_pipeline(prompt, num_users, runtime, model_choice)
    if sys.argv[1] == "roost":
        subprocess.run(["locust"], cwd=".")
    else:
        print("Usage: flk [fly (cli)|roost (web)]")


if __name__ == "__main__":
    main()
