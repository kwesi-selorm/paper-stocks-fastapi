from typing import Any, Mapping

from bson import ObjectId
from fastapi import HTTPException

from config.DatabaseConfig import DatabaseConfig
from model.UserModel import User

users_collection = DatabaseConfig().get_collection("users")


class UserService:
    @staticmethod
    def find_by_id(user_id: str):
        document: Mapping[str, Any] | None = users_collection.find_one({'_id': ObjectId(user_id)})
        if document is None:
            raise HTTPException(status_code=404, detail={"message": f"User with id '{user_id}' not found"})
        return document

    @staticmethod
    def find_by_email(email: str):
        document: Mapping[str, Any] | None = users_collection.find_one({'email': email})
        if document is None:
            raise HTTPException(status_code=404, detail={"message": f"User with email '{email}' found"})
        return document

    @staticmethod
    def find_by_username(username: str):
        document: Mapping[str, Any] | None = users_collection.find_one({'username': username})
        if not document:
            raise HTTPException(status_code=404, detail={"message": f"User with username '{username}' found"})
        return document

    @staticmethod
    def save(user: User):
        result = users_collection.insert_one(user.dict())
        return result.inserted_id

    @staticmethod
    def update_on_buy(user_id: str, update: dict[str, Any]):
        users_collection.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": update})
