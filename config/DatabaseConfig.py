import os

from dotenv import load_dotenv
from fastapi import HTTPException
from pymongo import MongoClient

load_dotenv()


class DatabaseConfig:
    @staticmethod
    def get_collection(collection_name):
        try:
            mongo_client = MongoClient(os.environ.get("MONGODB_URL"))
            database = mongo_client["fastapi"]
            return database[collection_name]
        except ConnectionError as e:
            print('Failed to connect to MongoDB', str(e))
            raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")
