import os

from dotenv import load_dotenv
from fastapi.responses import JSONResponse
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
            return JSONResponse(status_code=500, content={"message": "Failed to connect to MongoDB"})
