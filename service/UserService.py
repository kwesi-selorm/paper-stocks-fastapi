from typing import Any, Mapping

from bson import ObjectId
from fastapi import HTTPException

from config.DatabaseConfig import DatabaseConfig
from model.UserModel import User

users_collection = DatabaseConfig().get_collection("users")


def raise_exception(e: Exception) -> HTTPException:
    return HTTPException(status_code=500, detail={"message": "Error communicating with the database: " + str(e)})


class UserService:
    @staticmethod
    def find_by_id(user_id: str):
        try:
            document: Mapping[str, Any] | None = users_collection.find_one({'_id': ObjectId(user_id)})
            if not document:
                raise HTTPException(status_code=404, detail={"message": f"User with id '{user_id}' found"})
            return document
        except Exception as e:
            raise raise_exception(e)

    @staticmethod
    def find_by_email(email: str):
        try:
            document: Mapping[str, Any] | None = users_collection.find_one({'email': email})
            if not document:
                raise HTTPException(status_code=404, detail={"message": f"User with email '{email}' found"})
            return document
        except Exception as e:
            raise raise_exception(e)

    @staticmethod
    def find_by_username(username: str):
        try:
            document: Mapping[str, Any] | None = users_collection.find_one({'username': username})
            if not document:
                raise HTTPException(status_code=404, detail={"message": f"User with username '{username}' found"})
            return document
        except Exception as e:
            raise raise_exception(e)

    @staticmethod
    def save(user: User):
        try:
            result = users_collection.insert_one(user.dict())
            return result.inserted_id
        except Exception as e:
            raise raise_exception(e)

    @staticmethod
    def update_on_buy(user_id: str, update: dict[str, Any]):
        try:
            users_collection.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": update})
        except Exception as e:
            raise raise_exception(e)
