import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import HTTPException, status, Header
import jwt
from pydantic import BaseModel
from dotenv import load_dotenv

from service.UserService import UserService

load_dotenv()

SECRET = os.environ.get("JWT_SECRET_FASTAPI")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60

user_service = UserService()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail={"message": "Invalid or expired token, please login again"},
)


class Payload(BaseModel):
    username: str


def create_access_token(username: str) -> str:
    try:
        payload = {
            "sub": username,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        encoded_jwt = jwt.encode(payload, SECRET, ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Error generating access token: " + str(e)}
        )


def verify_access_token(authorization: Annotated[str | None, Header()]) -> None:
    token = authorization[7:] if authorization else None
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "No access token provided"},
        )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        user_doc = user_service.find_by_username(username)
        if user_doc is None:
            raise HTTPException(status_code=403, detail={"message": "No registered user found"})
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
