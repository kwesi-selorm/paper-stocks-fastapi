import json
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Body
from pydantic import BaseModel

from service.JWTService import JWTService
from service.UserService import UserService
from bson import json_util

router = APIRouter(prefix="/api/users", tags=["users"])
user_service = UserService()
jwt_service = JWTService()


class SignInInput(BaseModel):
    username: str
    password: str


class ReturnedUser:
    def __init__(self, _id: str, username: str, buying_power: int):
        self.id = _id
        self.username = username
        self.buyingPower = buying_power


class ReturnedUserWithToken(ReturnedUser):
    def __init__(self, _id: str, username: str, buying_power: int, token: str):
        super().__init__(_id, username, buying_power)
        self.token = token


@router.post("/signin")
async def signin(credentials: Annotated[SignInInput, Body(required=True)]):
    username = credentials.username
    print(username)
    user_doc = user_service.find_by_username(username)
    user_doc_json: dict = json.loads(json_util.dumps(user_doc))
    if not user_doc_json:
        raise HTTPException(status_code=404, detail={"message": "User not found"})

    access_token = jwt_service.create_access_token(username)
    return ReturnedUserWithToken(_id=str(user_doc_json["_id"]["$oid"]),
                                 username=user_doc_json["username"],
                                 buying_power=user_doc_json["buyingPower"],
                                 token=access_token)


@router.get("/get-user/{user_id}", dependencies=[Depends(JWTService.verify_access_token)])
async def get_user(user_id: str):
    try:
        doc = user_service.find_by_id(user_id)
        if not doc:
            raise HTTPException(status_code=404, detail={"message": "User not found"})
        doc_json = json.loads(json_util.dumps(doc))
        return ReturnedUser(
            _id=str(doc_json["_id"]["$oid"]),
            username=doc_json["username"],
            buying_power=doc_json["buyingPower"])

    except Exception as e:
        raise HTTPException(status_code=500, detail={"message": str(e)})
