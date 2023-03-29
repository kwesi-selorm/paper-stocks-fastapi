import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import HTTPException, status, Header
from fastapi.responses import JSONResponse
import jwt
from pydantic import BaseModel
from dotenv import load_dotenv
from starlette.responses import JSONResponse

from service.UserService import UserService

load_dotenv()

SECRET = os.environ.get("JWT_SECRET_FASTAPI")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60

user_service = UserService()

unauthorized_response = JSONResponse(
    status_code=status.HTTP_401_UNAUTHORIZED,
    content={"message": "Invalid or expired token, please login again"},
)


class Payload(BaseModel):
    username: str


def create_access_token(username: str):
    try:
        payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        if SECRET is None:
            raise HTTPException(
                status_code=500, detail={"message": "JWT_SECRET not set"}
            )
        encoded_jwt: str = jwt.encode(payload, SECRET, ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": "Error generating access token: " + str(e)},
        )


def verify_access_token(authorization: Annotated[str | None, Header()]):
    token = authorization[7:] if authorization else None
    if token is None:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "No access token provided"},
        )
    if SECRET is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "JWT_SECRET not set"},
        )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return unauthorized_response
        user_doc = user_service.find_by_username(username)
        if user_doc is None:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"message": "No registered user found"},
            )
    except jwt.ExpiredSignatureError:
        return unauthorized_response
    except jwt.InvalidTokenError:
        return unauthorized_response
