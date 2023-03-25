from pprint import pprint

from pymongo import MongoClient

from util.get_secrets import secrets


def connect_to_database():
    try:
        mongo_client = MongoClient(secrets.get('MONGODB_URL_DEV'))
        database = mongo_client["test"]
        print('Connected to MongoDB')
        return database
    except ConnectionError as e:
        print('Failed to connect to MongoDB', e)
        return None


db = connect_to_database()
