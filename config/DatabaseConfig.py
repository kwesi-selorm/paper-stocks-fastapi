from pymongo import MongoClient

from helper.secrets_helper import secrets


class DatabaseConfig:
    @staticmethod
    def get_collection(collection_name):
        try:
            mongo_client = MongoClient(secrets.get('MONGODB_URL_DEV'))
            database = mongo_client["fastapi"]
            return database[collection_name]
        except ConnectionError as e:
            print('Failed to connect to MongoDB', str(e))
            return None


def connect_to_database():
    try:
        mongo_client = MongoClient(secrets.get('MONGODB_URL_DEV'))
        database = mongo_client["fastapi"]
        print('Connected to MongoDB')
        return database
    except ConnectionError as e:
        print('Failed to connect to MongoDB', e)
        return None


db = connect_to_database()
