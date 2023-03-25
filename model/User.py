from bson import ObjectId
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    passwordHash: str
    passwordSalt: str
    passwordClue: str
    buyingPower: float
