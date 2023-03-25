from pprint import pprint

from pymongo import MongoClient

from helper.secrets_helper import secrets


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
