import json
from datetime import datetime
from typing import List


def clean_up_locust_data(raw_data: List[dict], guid: str) -> List[dict]:
    res = []

    for x in raw_data:
        data = {}
        data["session_id"] = guid
        data["url"] = x["url"]
        data["name"] = x["name"]
        data["request_type"] = x["request_type"]
        data["start_time"] = datetime.utcfromtimestamp(x["start_time"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        data["response_time"] = x["response_time"]
        data["response_length"] = x["response_length"]
        data["inference_time"] = x["response"]["inference_status"]["runtime_ms"]
        data["tokens_input"] = x["response"]["inference_status"]["tokens_input"]
        data["tokens_output"] = x["response"]["inference_status"]["tokens_generated"]
        data["cost"] = x["response"]["inference_status"]["cost"]
        data["response"] = x["response"]["results"][0]["generated_text"]
        # data["raw"] = x
        res.append(data)

    __write_cleaned_data(res)

    return res


def __write_cleaned_data(inference_data):
    file_path = "temp/flk_fly_inference_data_clean.json"
    with open(file_path, "w") as json_file:
        json.dump(inference_data, json_file)
