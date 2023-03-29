from typing import Any
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette import status


def validate_str(input: Any | None):
    if not isinstance(input, str) or len(input.strip()) == 0 or input is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Input must be a valid string"},
        )
    return input


def validate_int(input: Any | None):
    if not isinstance(input, int) or input <= 0 or input is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Input must be a positive integer"},
        )
    return input
