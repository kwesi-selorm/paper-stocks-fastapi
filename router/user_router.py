import json
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse

from auth.jwt_fns import create_access_token, verify_access_token
from model.UserModel import SignInUser, SignUpUser, User
from service.AssetService import AssetService
from service.UserService import UserService
from bson import json_util
from helper.password_helper import verify_password, hash_password

router = APIRouter(prefix="/api/users", tags=["users"])
user_service = UserService()
asset_service = AssetService()


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
async def signin(credentials: Annotated[SignInUser, Body(required=True)]):
    signin_input = credentials.dict()
    username_input = signin_input.get("username")
    if username_input is None:
        return JSONResponse(
            status_code=400, content={"message": "Username is required"}
        )
    password_input = signin_input.get("password")
    if password_input is None:
        return JSONResponse(
            status_code=400, content={"message": "Password is required"}
        )

    try:
        user_doc = user_service.find_by_username(username_input)

        if not user_doc:
            return JSONResponse(
                status_code=404,
                content={
                    "message": f"A user with the username '{username_input}' was not found"
                },
            )
        user_doc_json: dict = json.loads(json_util.dumps(user_doc))
        password_hash = user_doc_json["passwordHash"]

        if not verify_password(password_input, password_hash):
            return JSONResponse(
                status_code=401, content={"message": "Invalid password"}
            )
        access_token = create_access_token(username_input)
        return ReturnedUserWithToken(
            _id=str(user_doc_json["_id"]["$oid"]),
            username=user_doc_json["username"],
            buying_power=user_doc_json["buyingPower"],
            token=access_token,
        )
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": "Something went wrong: " + str(e)}
        )


@router.post("/signup")
async def signup(credentials: Annotated[SignUpUser, Body(required=True)]):
    signup_input = credentials.dict()
    username_input = signup_input.get("username")
    if username_input is None:
        return JSONResponse(
            status_code=400, content={"message": "Username is required"}
        )
    email_input = signup_input.get("email")
    if email_input is None:
        return JSONResponse(status_code=400, content={"message": "Email is required"})
    password_input = signup_input.get("password")
    if password_input is None:
        return JSONResponse(
            status_code=400, content={"message": "Password is required"}
        )

    try:
        existing_user_username = user_service.find_by_username(username_input)
        if existing_user_username:
            return JSONResponse(
                status_code=409,
                content={
                    "message": f"A user with username '{username_input}' already exists"
                },
            )
        existing_user_email = user_service.find_by_email(email_input)
        if existing_user_email:
            return JSONResponse(
                status_code=409,
                content={
                    "message": f"A user with email '{email_input}' already exists"
                },
            )

        password_hash = hash_password(password_input)
        buying_power = 100000
        to_save = User(
            username=username_input,
            email=email_input,
            passwordHash=password_hash,
            buyingPower=buying_power,
        )
        doc_id = user_service.save(to_save)
        access_token = create_access_token(username_input)
        return ReturnedUserWithToken(
            _id=str(doc_id),
            username=username_input,
            buying_power=buying_power,
            token=access_token,
        )
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": "Something went wrong: " + str(e)}
        )


@router.get("/get-user/{user_id}", dependencies=[Depends(verify_access_token)])
async def get_user(user_id: str):
    try:
        doc = user_service.find_by_id(user_id)

        if not doc:
            return JSONResponse(status_code=404, content={"message": "User not found"})
        doc_json = json.loads(json_util.dumps(doc))
        return ReturnedUser(
            _id=str(doc_json["_id"]["$oid"]),
            username=doc_json["username"],
            buying_power=doc_json["buyingPower"],
        )

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": "Something went wrong: " + str(e)}
        )
