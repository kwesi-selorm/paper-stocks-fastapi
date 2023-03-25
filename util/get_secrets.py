import json
import os.path
from pydantic import BaseModel


def get_secrets():
    filename: str = os.path.join("secrets.json")
    try:
        with open(filename, "r") as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


secrets = get_secrets()
