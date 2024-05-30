import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["Flock"]
collection = db["flk-fly-data"]

file_path = "temp/flk_fly_inference_data.json"


def save_to_mongo(data: dict):
    collection.insert_many(data)
    print("Saved to mongo successfully!\n")
