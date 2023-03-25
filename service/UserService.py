from typing import Any, Mapping

from bson import ObjectId

from config.database_config import db
from model.UserModel import User

users_collection = db['users']


class UserService:
    @staticmethod
    def find_by_id(user_id: str):
        document: Mapping[str, Any] | None = users_collection.find_one({'_id': ObjectId(user_id)})
        return document

    @staticmethod
    def find_by_email(email: str):
        document: Mapping[str, Any] | None = users_collection.find_one({'email': email})
        return document

    @staticmethod
    def find_by_username(username: str):
        document: Mapping[str, Any] | None = users_collection.find_one({'username': username})
        return document

    @staticmethod
    def save_user(user: User):
        # Check if the user already exists, update if it does and save new if it does now
        result = users_collection.insert_one(user)
        return result.inserted_id
