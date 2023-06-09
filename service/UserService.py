from typing import Any, Mapping

from bson import ObjectId
from fastapi import HTTPException

from config.DatabaseConfig import DatabaseConfig
from model.UserModel import User

try:
    users_collection = DatabaseConfig().get_collection("users")
except ConnectionError as e:
    print("Failed to connect to MongoDB", str(e))
    raise HTTPException(
        status_code=500, detail={"message": "Failed to connect to MongoDB"}
    )


class UserService:
    @staticmethod
    def find_by_id(user_id: str):
        document: Mapping[str, Any] | None = users_collection.find_one(
            {"_id": ObjectId(user_id)}
        )
        return document

    @staticmethod
    def find_by_email(email: str):
        document: Mapping[str, Any] | None = users_collection.find_one({"email": email})
        return document

    @staticmethod
    def find_by_username(username: str):
        document: Mapping[str, Any] | None = users_collection.find_one(
            {"username": username}
        )
        return document

    @staticmethod
    def save(user: User):
        result = users_collection.insert_one(user.dict())
        return result.inserted_id

    @staticmethod
    def update_on_buy(user_id: str, update: dict[str, Any]):
        users_collection.find_one_and_update(
            {"_id": ObjectId(user_id)}, {"$set": update}
        )
