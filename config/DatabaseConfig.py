import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class DatabaseConfig:
    @staticmethod
    def get_collection(collection_name):
        mongo_client = MongoClient(os.environ.get("MONGODB_URL"))
        database = mongo_client["fastapi"]
        return database[collection_name]
