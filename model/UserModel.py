import re

from pydantic import BaseModel, validator


class User(BaseModel):
    username: str
    email: str
    passwordHash: str
    buyingPower: float


class SignInUser(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})", v):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, one number, "
                "and one special character")
        return v


class SignUpUser(SignInUser):
    email: str
    password: str
    confirmPassword: str

    @validator("email")
    def validate_email(cls, v):
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", v):
            raise ValueError("Invalid email address")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})", v):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, one number, "
                "and one special character")
        return v

    @validator("confirmPassword")
    def validate_confirm_password(cls, v, values):
        if "password" in values and v != values["password"]:
            raise ValueError("Passwords do not match")
        return v
